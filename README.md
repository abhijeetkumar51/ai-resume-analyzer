# 🤖 AI Resume Analyzer

> An AI-powered ATS Resume Analyzer built with **Flask**, **Groq**, **Docker**, and **GitHub Actions CI/CD**.

[![CI/CD](https://github.com/abhijeetkumar51/ai-resume-analyzer/actions/workflows/main.yml/badge.svg)](https://github.com/abhijeetkumar51/ai-resume-analyzer/actions)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Groq](https://img.shields.io/badge/AI-Groq-orange)

---

## 🚀 What It Does

Upload your **resume PDF** + paste a **job description** → Get instant AI analysis:

- ✅ **ATS Score** (0–100)
- ✅ **Matching Skills** — skills you already have
- ✅ **Missing Skills** — skills to add
- ✅ **Strengths & Weaknesses**
- ✅ **Improvement Suggestions**
- ✅ **Job description optimizer** — structure role details or generate a clearly labeled starter draft from a role title

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI Model | Groq API (GPT-OSS 120B) |
| PDF Parsing | PyPDF2 |
| Frontend | HTML, CSS, Vanilla JS |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## Academic Submission Report

The current INT333 project report is available in both PDF and editable Word formats:

- [Project report (PDF)](static/AI_Resume_Analyzer_Project_Report.pdf)
- [Editable project report (Word)](static/AI_Resume_Analyzer_Project_Report.docx)

Fill in the student and faculty placeholders on the cover page before submission.

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
- A [Groq API key](https://console.groq.com/keys)

### Run Locally

```bash
git clone https://github.com/abhijeetkumar51/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
```

Set your API key in a `.env` file in `ai-resume-analyzer/`:
```bash
GROQ_API_KEY=your_key_here
```

Keep `.env` private; never commit or share your API key.

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

Pull requests run the unit tests and build the Docker image. A push to `main` runs the same checks, requires the repository secrets `DOCKER_USERNAME` and `DOCKER_TOKEN`, then logs in and publishes both `latest` and a commit-SHA image tag to Docker Hub. Set these secrets to a Docker Hub username and access token that can push to `abhijeetchy51/ai-resume-analyser`; the workflow fails with an explicit error if either secret is missing.

Render deploys from the repository using `render.yaml`. Connect the repository in Render, set `GROQ_API_KEY` in the Render service environment, and configure the service's health check path as `/health` (the Blueprint already declares it). The app binds to Render's `PORT` environment variable. No API key is stored in the repository or image.

## 🧰 INT333 DevOps starter

- `render.yaml` describes the Docker web service and its `/health` check.
- `terraform/` is reserved for external infrastructure managed with Terraform. Render's hosted service does not expose its machine for SSH or host configuration.
- `ansible/` includes a playbook to check the public Render URL from a control machine or CI runner. Set `SERVICE_URL` first.
- `puppet/` shows a package-management example for a Linux monitoring host that you administer yourself; it does not target Render.
- `nagios/` contains an HTTP check for the public Render hostname. Configure it on a separately managed Nagios server.

These tools complement Render's service-level deployment. They do not imply access to Render's underlying container host. See each folder's README for its intended use.

---

## 🔐 Security

- API keys are supplied through environment variables and must never be committed.
- Resume PDFs are parsed in memory, are not written to the project's uploads folder, and are not retained after the request.
- Before AI analysis, email addresses, phone numbers, street addresses, and links are removed. This does not guarantee full anonymization; names and other resume details may remain.
- The remaining resume text and job description are sent to Groq only after the user confirms the in-app disclosure. Review Groq's data-handling terms and do not submit information you are not comfortable sharing with the provider.
- API responses use no-store headers, and the Flask development debugger is disabled.

---

## 👨‍💻 Author

**Abhijeet Kumar**  
GitHub: [@abhijeetkumar51](https://github.com/abhijeetkumar51)

---

## 📄 License

MIT License
