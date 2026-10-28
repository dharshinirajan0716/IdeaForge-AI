# IdeaForge AI

An AI-powered college project idea generator using Python, Flask, HTML/CSS/JavaScript, and Groq.

## Run locally (Windows PowerShell)
1. Install Python 3.10+ and Git.
2. Open this folder in VS Code.
3. `python -m venv .venv`
4. `.venv\\Scripts\\Activate.ps1`
5. `python -m pip install -r requirements.txt`
6. `$env:GROQ_API_KEY="your_key_here"`
7. `python app.py`
8. Open http://127.0.0.1:5000

Get a key from https://console.groq.com/keys. Never commit your key to GitHub.

## GitHub
```bash
git init
git add .
git status
git commit -m "Build IdeaForge AI"
git branch -M main
```
Create an empty GitHub repository and then:
```bash
git remote add origin https://github.com/YOUR_USERNAME/ideaforge-ai.git
git push -u origin main
```

## Render
Build command: `pip install -r requirements.txt`
Start command: `gunicorn app:app`
Environment variables: `GROQ_API_KEY` (secret) and optionally `GROQ_MODEL=llama-3.3-70b-versatile`.

## Demo video (about 60 seconds)
Show the homepage, enter skills and domain, generate the ideas, scroll through features and roadmaps, and finish by showing the deployed URL.
