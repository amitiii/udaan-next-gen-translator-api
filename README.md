# Translation Service API

A comprehensive translation service built with FastAPI that provides text translation capabilities using Google Translate API with fallback mock translations.

## 🚀 Features

- **Single Text Translation**: Translate individual text strings
- **Bulk Translation**: Translate multiple texts in a single request
- **Language Detection**: Automatically detect the language of input text
- **Request Logging**: Comprehensive logging of all translation requests
- **Statistics**: Get translation usage statistics and analytics
- **Input Validation**: Robust validation for text length and language codes
- **Error Handling**: Comprehensive error handling with clear error messages
- **API Documentation**: Auto-generated Swagger UI and ReDoc documentation
- **Health Check**: Service health monitoring endpoint

## 📋 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- googletrans
- SQLite3 (built-in)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd translation_service
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python -m translation_service.main
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn translation_service.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🌐 API Endpoints

### Health Check
- **GET** `/health` - Service health status

### Mock Translation Endpoints (No API Key Required)
- **POST** `/api/v1/translate/mock` - Single text translation using mock service
- **POST** `/api/v1/translate/bulk/mock` - Bulk text translation using mock service

### Gemini Translation Endpoints (Requires GEMINI_API_KEY)
- **POST** `/api/v1/translate/gemini` - Single text translation using Gemini Flash LLM
- **POST** `/api/v1/translate/bulk/gemini` - Bulk text translation using Gemini Flash LLM

### Utility Endpoints
- **GET** `/api/v1/languages` - Get supported languages
- **POST** `/api/v1/detect` - Detect text language

### Analytics Endpoints
- **GET** `/api/v1/stats` - Get translation statistics
- **GET** `/api/v1/logs` - Get recent translation logs

### Documentation
- **GET** `/docs` - Swagger UI documentation
- **GET** `/redoc` - ReDoc documentation

## 📖 API Usage Examples

### Mock Translation (Single)

```bash
curl -X POST "http://localhost:8000/api/v1/translate/mock" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, how are you?",
       "target_lang": "ta"
     }'
```

**Response:**
```json
{
  "original_text": "Hello, how are you?",
  "translated_text": "Hello, how are you? (தமிழில்)",
  "target_lang": "ta"
}
```

### Mock Translation (Bulk)

```bash
curl -X POST "http://localhost:8000/api/v1/translate/bulk/mock" \
     -H "Content-Type: application/json" \
     -d '{
       "texts": ["Hello", "Goodbye", "Thank you"],
       "target_lang": "es"
     }'
```

**Response:**
```json
{
  "translations": [
    {
      "original_text": "Hello",
      "translated_text": "Hello (en español)",
      "target_lang": "es"
    },
    {
      "original_text": "Goodbye", 
      "translated_text": "Goodbye (en español)",
      "target_lang": "es"
    },
    {
      "original_text": "Thank you",
      "translated_text": "Thank you (en español)", 
      "target_lang": "es"
    }
  ]
}
```

### Gemini Translation (Single)

```bash
curl -X POST "http://localhost:8000/api/v1/translate/gemini" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, how are you?",
       "target_lang": "ta"
     }'
```

**Response:**
```json
{
  "original_text": "Hello, how are you?",
  "translated_text": "வணக்கம், எப்படி இருக்கிறீர்கள்?",
  "target_lang": "ta"
}
```

### Gemini Translation (Bulk)

```bash
curl -X POST "http://localhost:8000/api/v1/translate/bulk/gemini" \
     -H "Content-Type: application/json" \
     -d '{
       "texts": ["Hello", "Goodbye", "Thank you"],
       "target_lang": "es"
     }'
```

**Response:**
```json
{
  "translations": [
    {
      "original_text": "Hello",
      "translated_text": "Hola",
      "target_lang": "es"
    },
    {
      "original_text": "Goodbye", 
      "translated_text": "Adiós",
      "target_lang": "es"
    },
    {
      "original_text": "Thank you",
      "translated_text": "Gracias", 
      "target_lang": "es"
    }
  ]
}
```

### Language Detection

```bash
curl -X POST "http://localhost:8000/api/v1/detect" \
     -H "Content-Type: application/json" \
     -d '"Bonjour, comment allez-vous?"'
```

**Response:**
```json
{
  "text": "Bonjour, comment allez-vous?",
  "detected_language": "fr",
  "confidence": 0.95,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Get Statistics

```bash
curl "http://localhost:8000/api/v1/stats?days=7"
```

**Response:**
```json
{
  "stats": {
    "single_translations": {
      "total_requests": 150,
      "successful_requests": 148,
      "success_rate": 98.67,
      "avg_processing_time_ms": 245.5
    },
    "bulk_translations": {
      "total_requests": 25,
      "successful_requests": 24,
      "success_rate": 96.0,
      "avg_processing_time_ms": 1200.3,
      "total_texts_processed": 125
    },
    "top_languages": [
      {"language": "es", "count": 45},
      {"language": "fr", "count": 32},
      {"language": "de", "count": 28}
    ]
  },
  "period_days": 7,
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🔧 Configuration

### Environment Variables

- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: "false")
- `GEMINI_API_KEY`: Google Gemini Flash LLM API key (required for Gemini translations)
- `TRANSLATION_DB_PATH`: SQLite database path (default: "translation_logs.db")

### Database Configuration

The service uses SQLite for logging. The database file (`translation_logs.db`) is created automatically in the project root.

## 📊 Supported Languages

The service supports a wide range of languages including:

- **European Languages**: English, Spanish, French, German, Italian, Portuguese, Russian, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Turkish, Greek, etc.
- **Asian Languages**: Japanese, Korean, Chinese, Thai, Vietnamese, Hindi, Tamil, Telugu, Bengali, Urdu, etc.
- **Middle Eastern Languages**: Arabic, Hebrew, Persian, etc.
- **African Languages**: Swahili, Zulu, Afrikaans, etc.

## 🛡️ Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input parameters
- **500 Internal Server Error**: Translation service errors
- **422 Unprocessable Entity**: Validation errors

All errors return a consistent format:

```json
{
  "error": "Error message",
  "detail": "Additional error details"
}
```

## 📝 Logging

The service logs all translation requests with:

- Input text and target language
- Translation result
- Timestamp
- Client IP address
- Processing time
- Request status (success/error)

## 🧪 Testing

### Manual Testing

You can test the API using the interactive documentation:

1. Start the server: `python -m translation_service.main`
2. Open your browser and go to: `http://localhost:8000/docs`
3. Use the Swagger UI to test all endpoints

### Automated Testing

Create a test script to verify functionality:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_single_translation():
    response = requests.post(f"{BASE_URL}/api/v1/translate", json={
        "text": "Hello, how are you?",
        "target_lang": "ta"
    })
    print("Single Translation:", response.json())

def test_bulk_translation():
    response = requests.post(f"{BASE_URL}/api/v1/translate/bulk", json={
        "texts": ["Hello", "Goodbye"],
        "target_lang": "es"
    })
    print("Bulk Translation:", response.json())

if __name__ == "__main__":
    test_single_translation()
    test_bulk_translation()
```

## 🏗️ Project Structure

```
translation_service/
├── main.py                 # FastAPI application setup
├── routes/
│   └── translate.py        # API endpoints
├── services/
│   └── translator.py       # Translation logic
├── utils/
│   └── validators.py       # Input validation
├── db/
│   └── logger.py           # SQLite logging
├── models/
│   └── schemas.py          # Pydantic models
└── __init__.py
```

## 🔄 API Versioning

The API is versioned under `/api/v1/`. Future versions will be available under `/api/v2/`, etc.

## 🚀 Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "translation_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t translation-service .
docker run -p 8000:8000 translation-service
```

### Production Considerations

1. **Security**: Configure CORS properly for production
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **Authentication**: Add API key authentication
4. **Monitoring**: Set up proper monitoring and alerting
5. **Database**: Consider using a production database like PostgreSQL
6. **Caching**: Implement caching for frequently requested translations

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue in the repository. 

## 🔑 Environment Variables and Credentials

### Setting up your .env file

1. **Copy the template:**
   ```bash
   cp env_template.txt .env
   ```

2. **Edit the .env file** with your configuration:

```env
# Database Configuration
TRANSLATION_DB_PATH=translation_logs.db

# Google Translate API (Optional - for future use)
GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here

# Gemini Flash LLM API Key (Required for Gemini translations)
GEMINI_API_KEY=your_gemini_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=false

# Logging Configuration
LOG_LEVEL=info
LOG_FILE=translation_service.log

# Rate Limiting (optional)
MAX_REQUESTS_PER_MINUTE=60
MAX_TEXT_LENGTH=1000
MAX_BULK_TEXTS=10

# Cache Configuration
LANGUAGE_CACHE_DURATION=3600  # 1 hour in seconds
```

### Google Translate API Options

**Option 1: Free googletrans (Default)**
- No API key required
- Uses Google Translate's web interface
- Free but unofficial
- Good for development and testing
- Set `GOOGLE_TRANSLATE_API_KEY=` (empty)

**Option 2: Official Google Cloud Translate API**
- Requires Google Cloud account and API key
- Pay-per-use pricing ($20 per million characters)
- Guaranteed uptime and support
- Better for production use
- Set `GOOGLE_TRANSLATE_API_KEY=your_api_key_here`

### Getting a Google Cloud API Key (Optional)

If you want to use the official API:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the "Cloud Translation API"
4. Create credentials (API key)
5. Add the API key to your `.env` file

The service uses `python-dotenv` to load these variables automatically at startup.

## 🛠️ How the Flow Works (Udaan Assignment)

1. **Startup**: The service loads environment variables from `.env` for DB and API credentials.
2. **/health**: Simple endpoint to check if the service is running.
3. **/api/v1/translate**: Accepts a block of text (≤1000 chars) and a target language code. Validates input, fetches supported languages dynamically from Google Translate API, and performs the translation. Returns the result in JSON.
4. **/api/v1/translate/bulk**: Accepts an array of texts and a target language. Validates all inputs, performs bulk translation, and returns results in JSON.
5. **/api/v1/languages**: Returns the list of supported languages dynamically fetched from Google Translate API.
6. **/api/v1/detect**: Detects the language of a given text.
7. **Logging**: All translation requests are logged to the SQLite database (path from `.env`).
8. **Error Handling**: All endpoints provide clear error messages for invalid input, unsupported languages, or API errors.

**The service is modular:**
- `routes/` handles API endpoints
- `services/` contains translation logic (with dynamic language fetching)
- `db/` handles logging
- `utils/` provides validation helpers

**You can configure the DB path and Google API key without changing code, just by editing `.env`.**

## 🚀 Quick Start Guide

### **Option 1: Automated Setup (Recommended)**

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Run the service:**
   ```bash
   python run.py
   ```

### **Option 2: Manual Setup**

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   cp env_template.txt .env
   # Edit .env with your configuration
   ```

5. **Run the service:**
   ```bash
   python run.py
   # OR
   python -m app.main
   ```

## 🌐 Access the Service

Once running, the service will be available at:

- **Main API:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **Swagger UI (API Docs):** http://localhost:8000/docs
- **ReDoc (Alternative Docs):** http://localhost:8000/redoc

## 🧪 Test the Service

### **Quick Test with curl:**

```bash
# Health check
curl http://localhost:8000/health

# Single translation
curl -X POST "http://localhost:8000/api/v1/translate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, how are you?", "target_lang": "es"}'

# Get supported languages
curl http://localhost:8000/api/v1/languages
```

### **Test with Python:**

```bash
# Run the test script
python test_api.py
```

## 🔧 Troubleshooting

### **Common Issues:**

1. **Port already in use:**
   ```bash
   # Change port in .env
   PORT=8001
   ```

2. **Virtual environment not activated:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Dependencies not installed:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Permission denied (Linux/macOS):**
   ```bash
   chmod +x setup.py run.py
   ```

### **Logs and Debugging:**

- Check console output for error messages
- Database logs: `translation_logs.db` (SQLite file)
- API logs: Available in console and `/api/v1/logs` endpoint 