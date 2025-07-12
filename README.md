# 🕊️ Udaan Next-Gen – Translation Microservice

🚀 An advanced, modular, production-ready **FastAPI-based translation microservice** built for the IIT Bombay AI Engineer Research Internship.

---

## 🔍 Overview

This microservice accepts input text and a target language, translates the content using a **mock dictionary** (or plug-in LLM model like Groq or Google Translate), and returns the translated result. Designed with extensibility, modularity, and performance in mind.

> ✅ **Bonus Features**: Async bulk translation, SQLite logging, health check, Docker deployment, plug-and-play translator adapter, and test-ready structure.

---

## 🧠 Key Features

| Feature                    | Description |
|---------------------------|-------------|
| ✅ Single sentence translation | Translate one sentence using a mock or LLM backend |
| ✅ Bulk translation         | Translate multiple sentences asynchronously |
| ✅ Health check             | `/health` endpoint with version, uptime, and supported langs |
| ✅ SQLite logging           | Every translation request is stored with full auditability |
| ✅ ISO 639‑1 validation     | Ensures valid 2-letter language codes only |
| ✅ Plug-n-play architecture | Supports adapters for multiple translation engines |
| ✅ Dockerized               | Production-ready Dockerfile included |
| ✅ Pytest-based tests       | Ensures code quality & behavior verification |

---

## 📦 Supported Languages

- `hi` – Hindi  
- `ta` – Tamil  
- `bn` – Bengali  
- `kn` – Kannada  

---

## 📁 Project Structure

```
udaan-next-gen/
├── app/
│   ├── routes/           # API endpoints
│   ├── services/         # Translation logic
│   ├── adapters/         # Translation engine plugins (Mock / LLM)
│   ├── models/           # Request & Response schemas
│   ├── db/               # SQLite logging
│   └── main.py           # FastAPI entry point
├── tests/                # Pytest-based tests
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 API Usage

### 🔹 POST `/translate`

Translate a single block of text.

**Request:**
```json
{
  "text": "hello world",
  "target_lang": "hi"
}
```

**Response:**
```json
{
  "original_text": "hello world",
  "translated_text": "नमस्ते दुनिया",
  "target_lang": "hi"
}
```

---

### 🔹 POST `/translate/bulk`

Translate multiple sentences in one request.

**Request:**
```json
{
  "sentences": [
    {"text": "hello", "target_lang": "bn"},
    {"text": "world", "target_lang": "ta"}
  ]
}
```

**Response:**
```json
[
  {"original_text": "hello", "translated_text": "হ্যালো", "target_lang": "bn"},
  {"original_text": "world", "translated_text": "உலகம்", "target_lang": "ta"}
]
```

---

### 🔹 GET `/health`

Basic uptime and metadata check.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.2",
  "uptime": "00:10:04",
  "language_support": ["hi", "ta", "bn", "kn"]
}
```

---

## 💾 Translation Logs

Each translation request is logged to a local `SQLite` DB file (`translations.db`) containing:

- Original Text  
- Translated Text  
- Target Language  

Use `sqlite3 translations.db` to inspect or query.

---

## 🐳 Run with Docker

```bash
# Build
docker build -t udaan-next-gen .

# Run
docker run -p 8000:8000 udaan-next-gen
```

📍 Access Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✅ Setup Locally (Non-Docker)

```bash
git clone <your_repo_url>
cd udaan-next-gen
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🧪 Run Tests

```bash
pytest tests/
```
---

## 🏁 License

MIT License – Free to use with credit.
