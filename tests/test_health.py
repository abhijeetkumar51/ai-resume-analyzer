import unittest
from unittest.mock import Mock, patch

from app import GROQ_MODEL, app, call_groq


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


if __name__ == '__main__':
    unittest.main()
