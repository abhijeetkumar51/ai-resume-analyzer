# 🤖 AI Resume Analyzer

> An AI-powered ATS Resume Analyzer built with **Flask**, **Google Gemini**, **Docker**, and **GitHub Actions CI/CD**.

[![CI/CD](https://github.com/abhijeetkumar51/ai-resume-analyzer/actions/workflows/main.yml/badge.svg)](https://github.com/abhijeetkumar51/ai-resume-analyzer/actions)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-8E75B2)

---

## 🚀 What It Does

Upload your **resume PDF** + paste a **job description** → Get instant AI analysis:

- ✅ **ATS Score** (0–100)
- ✅ **Matching Skills** — skills you already have
- ✅ **Missing Skills** — skills to add
- ✅ **Strengths & Weaknesses**
- ✅ **Improvement Suggestions**

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI Model | Google Gemini API |
| PDF Parsing | PyPDF2 |
| Frontend | HTML, CSS, Vanilla JS |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## 📁 Project Structure

```
ai-resume-analyser/
├── app.py                    # Flask backend + Groq AI integration
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── templates/
│   └── index.html            # Frontend UI
└── .github/
    └── workflows/
        └── main.yml          # CI/CD pipeline
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.11+
- A [Gemini API key](https://aistudio.google.com/app/apikey)

### Run Locally

```bash
git clone https://github.com/abhijeetkumar51/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
```

Set your API key in a `.env` file in `ai-resume-analyzer/`:
```bash
GEMINI_API_KEY=your_key_here
```

Keep `.env` private; never commit or share your API key.

```bash
python app.py
```

Open **http://localhost:5000**

---

## 🐳 Run with Docker

```bash
docker run -p 5000:5000 -e GEMINI_API_KEY="your_key_here" abhijeetchy51/ai-resume-analyser:latest
```

Open **http://localhost:5000**

---

## 🔄 CI/CD Pipeline

On every push to `main`, GitHub Actions automatically:
1. Installs dependencies
2. Builds the Docker image
3. Pushes to Docker Hub → deployed live on **Render**

---

## 🔐 Security

- API keys are supplied through environment variables and must never be committed.
- Resume PDFs are parsed in memory, are not written to the project's uploads folder, and are not retained after the request.
- Before AI analysis, email addresses, phone numbers, street addresses, and links are removed. This does not guarantee full anonymization; names and other resume details may remain.
- The remaining resume text and job description are sent to Google Gemini only after the user confirms the in-app disclosure. Review Google's data-handling terms and do not submit information you are not comfortable sharing with the provider.
- API responses use no-store headers, and the Flask development debugger is disabled.

---

## 👨‍💻 Author

**Abhijeet Kumar**  
GitHub: [@abhijeetkumar51](https://github.com/abhijeetkumar51)

---

## 📄 License

MIT License
