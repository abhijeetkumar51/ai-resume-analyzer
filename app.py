import os
import json
import re
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    return text.strip()


def analyze_resume_with_gemini(resume_text, job_description):
    """Send resume and job description to Gemini AI for analysis."""
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY environment variable is not set.")

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
You are an expert ATS (Applicant Tracking System) and HR specialist.
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

Return ONLY the JSON object, no markdown, no explanation, no code blocks.
"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

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

    # Analyze with Gemini
    result = analyze_resume_with_gemini(resume_text, job_description)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
