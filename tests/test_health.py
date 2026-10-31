import unittest
from html.parser import HTMLParser
from unittest.mock import Mock, patch

from app import GROQ_MODEL, app, call_groq, is_role_title_only


class ReportLayoutParser(HTMLParser):
    panel_ids = {'panel-overview', 'panel-skills', 'panel-strengths', 'panel-suggestions'}

    def __init__(self):
        super().__init__()
        self.visible_panels = {}
        self.tab_count = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        panel_id = attributes.get('id')
        if panel_id in self.panel_ids:
            self.visible_panels[panel_id] = 'hidden' not in attributes
        if attributes.get('role') == 'tab':
            self.tab_count += 1


class HealthEndpointTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health_returns_ok_json(self):
        response = self.client.get('/health')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('status'), 'ok')
        self.assertIn('ai_configured', data)
        self.assertEqual(response.headers['Cache-Control'], 'no-store')


class ReportLayoutTests(unittest.TestCase):
    def test_analysis_sections_are_visible_without_tabs(self):
        response = app.test_client().get('/')
        parser = ReportLayoutParser()
        parser.feed(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(parser.visible_panels), parser.panel_ids)
        self.assertTrue(all(parser.visible_panels.values()))
        self.assertEqual(parser.tab_count, 0)


class GroqModelTests(unittest.TestCase):
    def test_call_groq_uses_current_default_model(self):
        client = Mock()
        client.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content='ok'))
        ]

        with patch('app.get_client', return_value=client):
            result = call_groq('prompt', 'system instruction')

        self.assertEqual(result, 'ok')
        client.chat.completions.create.assert_called_once()
        self.assertEqual(
            client.chat.completions.create.call_args.kwargs['model'],
            'openai/gpt-oss-120b',
        )
        self.assertEqual(GROQ_MODEL, 'openai/gpt-oss-120b')


class JobDescriptionOptimizerTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_short_role_title_is_expanded_as_a_labeled_draft(self):
        draft = (
            'Role Summary\n- Support reliable software delivery.\n'
            'Required Skills\n- CI/CD fundamentals.'
        )
        with patch('app.get_api_key', return_value='test-key'), patch(
            'app.call_groq', return_value=draft
        ) as call_groq_mock:
            response = self.client.post(
                '/optimize',
                json={'job_description': 'DevOps Engineer', 'consent': True},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'optimized': draft, 'is_draft': True})
        prompt = call_groq_mock.call_args.args[0]
        self.assertIn('only a job title', prompt)
        self.assertIn('general AI-generated draft', prompt)
        self.assertIn('Responsibilities', prompt)
        self.assertTrue(is_role_title_only('DevOps Engineer'))
        self.assertFalse(is_role_title_only('Build and maintain CI/CD pipelines'))

    def test_detailed_description_keeps_original_requirements(self):
        description = (
            'Build CI/CD pipelines with GitHub Actions. '
            'Manage AWS infrastructure using Terraform.'
        )
        with patch('app.get_api_key', return_value='test-key'), patch(
            'app.call_groq', return_value='Structured description'
        ) as call_groq_mock:
            response = self.client.post(
                '/optimize',
                json={'job_description': description, 'consent': True},
            )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.get_json()['is_draft'])
        prompt = call_groq_mock.call_args.args[0]
        self.assertIn('Keep ALL original requirements; never invent new ones.', prompt)
        self.assertIn(description, prompt)
        self.assertFalse(is_role_title_only(description))


if __name__ == '__main__':
    unittest.main()
