# 🌐 Udaan Next-Gen Translator API

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)

**Udaan Next-Gen Translator API** is a lightweight, production-grade microservice built with FastAPI to translate text and documents using OpenAI GPT models. It supports `.txt`, `.pdf`, and `.docx` files and is fully containerized using Docker.

---

## 🚀 Features

- 🌍 Translate between any OpenAI-supported languages
- 📁 Translate `.txt`, `.pdf`, and `.docx` files
- 🧠 Uses GPT-3.5 / GPT-4 via OpenAI API
- 🧪 Health check endpoint
- 🐳 Dockerized microservice
- 🔒 Environment-based API key configuration
- 📦 Modular and scalable architecture

---

## 📁 Project Structure

```
udaan-next-gen-translator-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment variable handling
│   ├── utils/
│   │   ├── translator.py    # GPT-based translation logic
│   │   ├── file_handler.py  # PDF, DOCX, TXT reading
│   │   └── logger.py        # Logging setup
│   └── routers/
│       └── routes.py        # API endpoints
├── requirements.txt         # Project dependencies
├── Dockerfile               # Docker configuration
├── .env.example             # Environment variable example
└── README.md                # Project documentation
```

---

## 🧪 API Endpoints

| Method | Endpoint          | Description                |
|--------|-------------------|----------------------------|
| GET    | `/health`         | Health check               |
| POST   | `/translate`      | Translate plain text       |
| POST   | `/translate-file` | Translate uploaded file    |

---

## 🔧 Setup & Installation

### ✅ Prerequisites

- Python 3.9+
- OpenAI API key
- Docker (optional)

### 🔨 Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/amitiii/udaan-next-gen-translator-api.git
   cd udaan-next-gen-translator-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the root directory:

   ```
   OPENAI_API_KEY=your_openai_api_key
   MODEL_NAME=gpt-4
   ```

5. **Run the API**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🐳 Docker Deployment

1. **Build the image**
   ```bash
   docker build -t udaan-translator-api .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 8000:8000 --env-file .env udaan-translator-api
   ```

3. **Access API**
   Open in browser: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📄 Sample Request - `/translate`

### Request (JSON)
```json
POST /translate
Content-Type: application/json

{
  "source_text": "Hello, how are you?",
  "target_language": "Hindi"
}
```

### Response (JSON)
```json
{
  "translated_text": "नमस्ते, आप कैसे हैं?"
}
```

---

## 📄 Sample Request - `/translate-file`

Use Postman or curl to upload a file with `multipart/form-data`:

- **file**: The document (PDF/DOCX/TXT)
- **target_language**: e.g., `"Spanish"`

---

## 🔍 Testing

Health check:
```bash
curl -X GET http://localhost:8000/health
```

Docs:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Tech Stack

- **FastAPI** - API Framework
- **OpenAI GPT-4 / GPT-3.5** - Translation engine
- **PyMuPDF** - PDF parsing
- **python-docx** - DOCX parsing
- **Uvicorn** - ASGI server
- **Docker** - Containerization

---

## 🙋‍♂️ Author

**Amiti Sharma**  
GitHub: [@amitiii](https://github.com/amitiii)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🔮 Future Enhancements

- 🌐 Auto language detection
- ⚡ Caching translations
- 🧾 Translation history logs
- 🔐 API key rate limiting and user auth
- 🌐 Frontend integration

---





