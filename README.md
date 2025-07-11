# 🌐 Udaan Next-Gen Translator API

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)

**Udaan Next-Gen Translator API** is a production-ready microservice built with FastAPI that enables language translation using OpenAI’s GPT models. It supports multiple input formats and includes comprehensive support for PDF, DOCX, TXT file translation, logging, health checks, and Dockerized deployment.

---

## 🚀 Features

- 🌍 Translate text between any languages supported by OpenAI
- 📁 Translate files: `.txt`, `.pdf`, `.docx`
- 🧠 Uses GPT-4 / GPT-3.5 via OpenAI API for contextual translation
- 🧪 Health check endpoint (`/health`)
- 📦 Modular, scalable microservice architecture
- 🔐 Environment-based secrets handling
- 🐳 Dockerized for easy deployment

---

---

## 📦 Installation

### 🔧 Prerequisites

- Python 3.9+
- OpenAI API Key
- Docker (optional)

### 🔨 Setup Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/amitiii/udaan-next-gen-translator-api.git
   cd udaan-next-gen-translator-api
2. **Create and activate a virtual environment**
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install_dependencies**
   
bash 
pip install -r requirements.txt

4. **Set up environment variables**
   Create a .env file using .env.example as a template.

ini
OPENAI_API_KEY=your-openai-key
MODEL_NAME=gpt-4

5. **run the api**

bash
uvicorn app.main:app --reload

🧪 API Endpoints
Method	Endpoint	Description
GET	/health	Health check endpoint
POST	/translate	Translate raw text
POST	/translate-file	Translate uploaded file

📄 Sample /translate Request
bash
POST /translate
Content-Type: application/json

{
  "source_text": "Hello, how are you?",
  "target_language": "Hindi"
}

🐳 Docker Deployment
🧱 Build Image
bash
docker build -t udaan-translator-api .
🚢 Run Container
bash
docker run -d -p 8000:8000 --env-file .env udaan-translator-api
Access API at: http://localhost:8000

✅ Testing
To test endpoints:

bash
curl -X GET http://localhost:8000/health
For file uploads and text translation, use Postman or Swagger UI at:
http://localhost:8000/docs

📚 Tech Stack
FastAPI - Web framework

OpenAI GPT-4/GPT-3.5 - Translation engine

Python - Core language

PyMuPDF, python-docx - File parsing

Uvicorn - ASGI server

Docker - Containerization





