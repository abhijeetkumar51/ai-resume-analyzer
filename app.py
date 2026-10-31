import io
import json
import logging
import os
import re
from dotenv import load_dotenv
from flask import Flask, Request, request, render_template, jsonify
from flask_cors import CORS
from groq import Groq
import PyPDF2


class InMemoryRequest(Request):
    """Keep uploaded file bodies in memory instead of Werkzeug's temp files."""

    def _get_file_stream(
        self, total_content_length, content_type, filename=None, content_length=None
    ):
        return io.BytesIO()


# Load .env file automatically if present (next to this file, not just cwd)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger('careerly')

app = Flask(__name__)
app.request_class = InMemoryRequest
CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')


def get_api_key():
    """Read Groq API key from environment at request time."""
    for name in ('GROQ_API_KEY', 'GEMINI_API_KEY'):
        key = os.environ.get(name, '').strip().strip('"').strip("'")
        if key and key != 'your_key_here':
            return key
    return ''


def get_client():
    api_key = get_api_key()
    if not api_key:
        raise Exception(
            "GROQ_API_KEY is not set. Create a .env file next to app.py with: GROQ_API_KEY=your_key"
        )
    return Groq(api_key=api_key)


def call_groq(prompt, system_instruction, temperature=0.3, max_output_tokens=2048):
    """Send a prompt to Groq and return the cleaned text response."""
    client = get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_output_tokens,
    )
    text = (response.choices[0].message.content or '').strip()
    # Strip markdown code fences if present
    text = re.sub(r'^```(?:json|text|markdown)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return text


def extract_text_from_pdf(pdf_path):
    """Extract text from an uploaded PDF stream without persisting the file."""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception:
        raise ValueError("Could not read this PDF. Please try another file.")
    return text.strip()


def redact_personal_data(text):
    """Remove common direct identifiers before sending text to the AI provider."""
    text = re.sub(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b', '[email removed]', text)
    text = re.sub(
        r'https?://\S+|www\.\S+|'
        r'\b(?:[\w-]+\.)+(?:com|org|net|io|dev|me|co|in|edu|gov|info|app|ai)(?:/\S*)?',
        '[link removed]',
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r'(?im)^\s*\d{1,6}\s+[\w .\'-]{2,50}\s+'
        r'(?:street|st|road|rd|avenue|ave|boulevard|blvd|lane|ln|drive|dr)\b.*$',
        '[address removed]',
        text,
    )

    def redact_phone(match):
        return '[phone removed]' if sum(char.isdigit() for char in match.group()) >= 10 else match.group()

    return re.sub(r'(?<!\w)\+?[\d(][\d\s().-]{7,}\d(?!\w)', redact_phone, text)


@app.after_request
def add_privacy_headers(response):
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; connect-src 'self'; "
        "img-src 'self' data:; font-src 'self'; base-uri 'none'; "
        "form-action 'self'; frame-ancestors 'none'"
    )
    return response


def analyze_resume_with_ai(resume_text, job_description):
    """Send resume and job description to Groq for analysis."""
    resume_text = redact_personal_data(resume_text)
    job_description = redact_personal_data(job_description)
    prompt = f"""You are an expert ATS (Applicant Tracking System) and HR specialist.
Analyze the following resume against the job description provided.
Do not repeat or infer the candidate's name, contact details, or other direct identifiers in the report.

Return your analysis ONLY as a valid JSON object with EXACTLY this structure:
{{
  "ats_score": <integer between 0 and 100>,
  "matching_skills": [<list of matching skill strings>],
  "missing_skills": [<list of missing skill strings>],
  "strengths": [<list of strength strings>],
  "weaknesses": [<list of weakness strings>],
  "suggestions": [<list of improvement suggestion strings>],
  "summary": "<brief 2-3 sentence overall assessment>"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY the JSON object, no markdown, no explanation, no code blocks."""

    raw = call_groq(
        prompt,
        system_instruction="You are an expert ATS resume analyzer. Always respond with valid JSON only.",
        temperature=0.3,
        max_output_tokens=2048,
    )

    result = None
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.exception('Groq returned non-JSON output (model=%s, length=%d): %s', GROQ_MODEL, len(raw), exc)
        raise ValueError('AI returned an invalid analysis. Please try again.') from exc
    if not isinstance(result, dict):
        logger.warning('Groq returned non-dict JSON (model=%s, type=%s)', GROQ_MODEL, type(result).__name__)
        raise ValueError('AI returned an invalid analysis.')

    for key, value in result.items():
        if isinstance(value, str):
            result[key] = redact_personal_data(value)
        elif isinstance(value, list):
            result[key] = [
                redact_personal_data(item) if isinstance(item, str) else item
                for item in value
            ]
    return result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Report that the Flask process is ready to serve HTTP requests."""
    return jsonify({'status': 'ok', 'ai_configured': bool(get_api_key())}), 200


@app.route('/optimize', methods=['POST'])
def optimize_prompt():
    """Rewrite a raw job description into a structured, ATS-friendly prompt."""
    data = request.get_json(silent=True) or {}
    jd = (data.get('job_description') or '').strip()

    if not jd:
        return jsonify({'error': 'Job description cannot be empty.'}), 400

    if data.get('consent') is not True:
        return jsonify({'error': 'Please confirm the AI data-sharing notice before continuing.'}), 400

    jd = redact_personal_data(jd)
    api_key = get_api_key()
    if not api_key:
        return jsonify({
            'error': 'AI is not configured on the server: GROQ_API_KEY is missing. Add it to the .env file next to app.py (or Render env vars) and restart the server.'
        }), 500

    try:
        optimized = call_groq(
            f"""Rewrite the following raw job description into a clean, structured, ATS-optimized version.

Rules:
- Keep ALL original requirements; never invent new ones.
- Organize under these headings: "Role Summary", "Required Skills", "Nice-to-Have Skills", "Responsibilities", "Qualifications".
- Use concise bullet points.
- Mention explicit years of experience and education only if present in the original.
- Output plain text only, no markdown code fences, no commentary.

RAW JOB DESCRIPTION:
{jd}""",
            system_instruction="You are an expert technical recruiter and prompt engineer. You rewrite messy job descriptions into clear, structured, ATS-friendly ones.",
            temperature=0.4,
            max_output_tokens=1200,
        )
        return jsonify({'optimized': optimized})
    except Exception as exc:
        logger.exception('Job description optimization failed (model=%s): %s', GROQ_MODEL, exc)
        return jsonify({'error': f'AI optimization failed: {exc}. Please try again.'}), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    # Validate file upload
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded.'}), 400

    file = request.files['resume']
    job_description = request.form.get('job_description', '').strip()

    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported.'}), 400

    if not job_description:
        return jsonify({'error': 'Job description cannot be empty.'}), 400

    if request.form.get('consent') != 'true':
        return jsonify({'error': 'Please confirm the AI data-sharing notice before continuing.'}), 400

    # Parse from the request stream; never write the uploaded resume to disk.
    try:
        resume_text = extract_text_from_pdf(file.stream)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    if not resume_text:
        return jsonify({'error': 'Could not extract text from the PDF. Ensure it is not a scanned image.'}), 400

    # Analyze with Groq AI
    if not get_api_key():
        return jsonify({
            'error': 'AI is not configured on the server: GROQ_API_KEY is missing. Add it to the .env file next to app.py (or Render env vars) and restart the server.'
        }), 500
    try:
        result = analyze_resume_with_ai(resume_text, job_description)
        return jsonify(result)
    except ValueError as exc:
        # Bad AI output (e.g. non-JSON): tell the user directly, still log it.
        logger.warning('Resume analysis returned invalid data (model=%s): %s', GROQ_MODEL, exc)
        return jsonify({'error': str(exc)}), 500
    except Exception as exc:
        # Real errors (bad key, bad model name, quota, network): log the full
        # traceback server-side, show the message safely in the response.
        logger.exception('Resume analysis failed (model=%s): %s', GROQ_MODEL, exc)
        return jsonify({'error': f'Resume analysis failed: {exc}'}), 500


if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST', '127.0.0.1'),
        port=int(os.environ.get('PORT', '5000')),
        debug=False,
    )
