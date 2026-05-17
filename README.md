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
├── app.py                    # Flask backend + Groq AI
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── .dockerignore             # Docker ignore rules
├── .gitignore                # Git ignore rules
├── .env.example              # Environment variable template
├── uploads/                  # Temporary PDF storage
├── static/                   # Static assets
├── templates/
│   └── index.html            # Frontend UI
└── .github/
    └── workflows/
        └── main.yml          # GitHub Actions CI/CD
```

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/abhijeetkumar51/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\Activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Groq API key
Get a free key at https://console.groq.com/keys
```bash
# Windows PowerShell
$env:GROQ_API_KEY = "gsk_your_key_here"

# Mac/Linux
export GROQ_API_KEY="gsk_your_key_here"
```

### 5. Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 🐳 Docker Setup

### Build image
```bash
docker build -t ai-resume-analyser .
```

### Run container
```bash
docker run -p 5000:5000 -e GROQ_API_KEY="gsk_your_key_here" ai-resume-analyser
```

Open **http://localhost:5000** in your browser.

---

## 🔄 CI/CD Pipeline

On every push to `main`, GitHub Actions automatically:
1. ✅ Installs dependencies
2. ✅ Verifies app syntax
3. ✅ Builds Docker image
4. ✅ Pushes to Docker Hub

### Required GitHub Secrets
| Secret | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password |

---

## 🌐 Deployment (Render)

1. Go to [render.com](https://render.com) → New Web Service
2. Connect GitHub → Select this repo
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
4. Add environment variable: `GROQ_API_KEY`
5. Click Deploy

---

## 🔐 Security

- API keys stored as environment variables (never hardcoded)
- `.env` file is gitignored
- Uploaded PDFs are temporary and not committed
- `.dockerignore` prevents secrets from entering Docker image

---

## 👨‍💻 Author

**Abhijeet Kumar**  
GitHub: [@abhijeetkumar51](https://github.com/abhijeetkumar51)

---

## 📄 License

MIT License
