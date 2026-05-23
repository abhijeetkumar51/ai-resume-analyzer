# 🤖 AI Resume Analyzer

> An AI-powered ATS Resume Analyzer built with **Flask**, **Groq AI (LLaMA 3.3 70B)**, **Docker**, and **GitHub Actions CI/CD**.

[![CI/CD](https://github.com/abhijeetkumar51/ai-resume-analyzer/actions/workflows/main.yml/badge.svg)](https://github.com/abhijeetkumar51/ai-resume-analyzer/actions)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange)

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
| AI Model | Groq API (LLaMA 3.3 70B) |
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
- A free [Groq API key](https://console.groq.com/keys)

### Run Locally

```bash
git clone https://github.com/abhijeetkumar51/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
```

Set your API key:
```bash
# Windows
$env:GROQ_API_KEY = "your_key_here"

# Mac/Linux
export GROQ_API_KEY="your_key_here"
```

```bash
python app.py
```

Open **http://localhost:5000**

---

## 🐳 Run with Docker

```bash
docker run -p 5000:5000 -e GROQ_API_KEY="your_key_here" abhijeetchy51/ai-resume-analyser:latest
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

- API keys are injected via environment variables — never hardcoded
- Uploaded PDFs are temporary and never committed to the repository

---

## 👨‍💻 Author

**Abhijeet Kumar**  
GitHub: [@abhijeetkumar51](https://github.com/abhijeetkumar51)

---

## 📄 License

MIT License
