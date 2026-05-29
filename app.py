import os
import json
import re
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from groq import Groq
import PyPDF2

# Load .env file automatically if present
load_dotenv()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def get_api_key():
    """Read Groq API key from environment at request time."""
    return os.environ.get('GROQ_API_KEY', '').strip()


def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    return text.strip()


def analyze_resume_with_groq(resume_text, job_description):
    """Send resume and job description to Groq AI for analysis."""
    api_key = get_api_key()
    if not api_key:
        raise Exception("GROQ_API_KEY is not set. Edit C:\\Ai-Resume-Analyser\\.env and add your key: GROQ_API_KEY=gsk_...")


    client = Groq(api_key=api_key)

    prompt = f"""You are an expert ATS (Applicant Tracking System) and HR specialist.
Analyze the following resume against the job description provided.

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

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert ATS resume analyzer. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=2048,
    )

    raw = chat_completion.choices[0].message.content.strip()

    # Strip markdown code fences if present
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    result = json.loads(raw)
    return result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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

    # Save the uploaded PDF
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resume.pdf')
    file.save(pdf_path)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text:
        return jsonify({'error': 'Could not extract text from the PDF. Ensure it is not a scanned image.'}), 400

    # Analyze with Groq AI
    try:
        result = analyze_resume_with_groq(resume_text, job_description)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
