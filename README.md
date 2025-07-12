# 🕊️ Udaan Next-Gen – Translation Microservice

🚀 An advanced, modular, production-ready **FastAPI-based translation microservice** built for the IIT Bombay AI Engineer Research Internship.

---

## 🔍 Overview

This microservice accepts input text and a target language, translates the content using a **mock dictionary** (or plug-in LLM model like Groq or Google Translate), and returns the translated result. Designed with extensibility, modularity, and performance in mind.

> ✅ **Bonus Features**: Async bulk translation, SQLite logging, health check, Docker deployment, plug-and-play translator adapter, and test-ready structure.

---
Table of Contents
Features

Project Structure

Setup and Installation

Running the Application

API Endpoints

GET /health

POST /api/v1/translate

POST /api/v1/bulk-translate

Pluggable Translation Engines

Database Logging

Running Tests

Deployment

Future Enhancements

License

Features
FastAPI Framework: High-performance, easy-to-use API development with automatic OpenAPI documentation.

Modular Architecture: Clear separation of concerns (API, core logic, database, models, plugins) for enhanced maintainability.

Pluggable Translation Engines: Easily switch between a Mock engine, an LLM-based engine, or integrate a real Google Translate API.

Robust Input Validation: Utilizes Pydantic models for strict request and response schema validation, ensuring data integrity.

Comprehensive Logging: Persists all translation requests and their responses to an SQLite database for auditing and analysis.

Health Check Endpoint: A dedicated /health endpoint for quick service status monitoring.

Bulk Translation Support: Efficiently translates multiple texts in a single API request.

Asynchronous Operations: Leverages FastAPI's async/await capabilities for non-blocking I/O, improving concurrency and performance.

Automated API Documentation: Self-generating interactive API documentation (Swagger UI) at /docs and ReDoc at /redoc.

Containerization Ready: Includes a Dockerfile for seamless building and deployment in containerized environments.

Unit Tests: Comprehensive test suite using pytest to ensure reliability and correctness of the application logic.

Project Structure
.
├── app/
│   ├── api/                    # Defines FastAPI routes and endpoints
│   │   ├── __init__.py
│   │   └── v1/                 # Versioned API endpoints
│   │       ├── __init__.py
│   │       └── endpoints.py    # Main API endpoints (translate, bulk-translate, health)
│   ├── core/                   # Core application logic and configurations
│   │   ├── __init__.py
│   │   ├── config.py           # Application settings and configurations
│   │   └── translation_engine.py # Abstract base class for translation engines
│   ├── db/                     # Database setup and operations
│   │   ├── __init__.py
│   │   └── database.py         # SQLite database connection and logging functions
│   ├── models/                 # Pydantic models for request/response schemas
│   │   ├── __init__.py
│   │   └── schemas.py          # Defines data structures for API interactions
│   ├── plugins/                # Pluggable translation engine implementations
│   │   ├── __init__.py
│   │   ├── llm_engine.py       # LLM-based translation engine (example)
│   │   └── mock_engine.py      # Mock translation engine (default for demo)
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   └── test_api.py             # Tests for API endpoints
├── Dockerfile                  # Docker build instructions
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation


Setup and Installation
Clone the repository:

git clone https://github.com/amitiii/udaan-next-gen-translator-api.git
cd udaan-next-gen-translator-api

Create a virtual environment (recommended):

python -m venv venv

Activate the virtual environment:

On macOS/Linux:

source venv/bin/activate

On Windows:

.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Running the Application
Ensure your virtual environment is activated.

Run the FastAPI application using Uvicorn:

uvicorn app.main:app --reload

The --reload flag enables auto-reloading on code changes, which is useful for development.

Access the API documentation:
Once the server is running, open your web browser and navigate to:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

API Endpoints
GET /health
Checks the health status of the microservice.

URL: /health

Method: GET

Example Request:

curl -X GET "http://127.0.0.1:8000/health" -H "accept: application/json"

Example Success Response:

{
  "status": "healthy",
  "timestamp": "2023-10-27T10:00:00.000000"
}

POST /api/v1/translate
Translates a single block of text.

URL: /api/v1/translate

Method: POST

Request Body:

text (string): The text to translate. Maximum 1000 characters.

target_language (string): The ISO 639-1 code of the target language (e.g., es for Spanish, hi for Hindi, ta for Tamil).

Example Request:

curl -X POST "http://127.0.0.1:8000/api/v1/translate" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Hello, how are you?",
           "target_language": "es"
         }'

Example Success Response (200 OK):

{
  "original_text": "Hello, how are you?",
  "translated_text": "¿Cómo estás?",
  "source_language": "en",
  "target_language": "es",
  "translation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}

Example Error Response (400 Bad Request - Invalid Language):

{
  "detail": "Invalid target language code: 'xyz'. Supported languages: en, es, fr, de, hi, ta, kn, bn."
}

Example Error Response (422 Unprocessable Entity - Validation Error):

{
  "detail": [
    {
      "type": "string_too_long",
      "loc": [
        "body",
        "text"
      ],
      "msg": "String should have at most 1000 characters",
      "input": "...",
      "ctx": {
        "max_length": 1000
      }
    }
  ]
}

POST /api/v1/bulk-translate
Translates an array of texts.

URL: /api/v1/bulk-translate

Method: POST

Request Body:

texts (array of strings): An array of texts to translate. Each text has a maximum of 1000 characters.

target_language (string): The ISO 639-1 code of the target language for all texts.

Example Request:

curl -X POST "http://127.0.0.1:8000/api/v1/bulk-translate" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
           "texts": [
             "Good morning.",
             "What time is it?"
           ],
           "target_language": "fr"
         }'

Example Success Response (200 OK):

{
  "translations": [
    {
      "original_text": "Good morning.",
      "translated_text": "Bonjour.",
      "source_language": "en",
      "target_language": "fr",
      "translation_id": "guid-1"
    },
    {
      "original_text": "What time is it?",
      "translated_text": "Quelle heure est-il ?",
      "source_language": "en",
      "target_language": "fr",
      "translation_id": "guid-2"
    }
  ]
}

Example Error Response: Similar to /api/v1/translate for individual text validation errors or invalid language codes.

Pluggable Translation Engines
The service is designed with a flexible plugin architecture for its translation capabilities. This allows easy swapping between different translation sources without modifying the core service logic.

Currently supported engines:

Mock Engine (mock_engine.py): A simple dictionary-based mock for demonstration and testing purposes. This is the default engine.

LLM Engine (llm_engine.py): Integrates with a Large Language Model (LLM) for translation. This engine would require specific LLM API setup and credentials.

To switch between engines, modify the TRANSLATION_ENGINE setting in app/core/config.py (or use an environment variable if configured). For example:

# app/core/config.py
# To use the LLM engine:
TRANSLATION_ENGINE = "llm"

# To use the Mock engine:
# TRANSLATION_ENGINE = "mock"

Database Logging
All translation requests and their corresponding responses are logged to an SQLite database file named translations.db (created in the project root).

The translation_logs table stores the following information:

id: Unique identifier for the log entry.

original_text: The input text provided by the user.

translated_text: The text returned by the translation engine.

source_language: The detected (or assumed) source language.

target_language: The requested target language.

timestamp: When the translation request was processed (UTC).

is_bulk: A boolean flag indicating if the request was part of a bulk translation.

You can inspect the database using any SQLite browser tool (e.g., DB Browser for SQLite).

Running Tests
The project includes a comprehensive suite of unit and integration tests using pytest.

Activate your virtual environment.

Navigate to the project root directory.

Run pytest:

pytest

Deployment
The application is containerized using Docker, making it easy to build and deploy in various environments.

Build the Docker image:
Navigate to the project root directory where the Dockerfile is located.

docker build -t translator-microservice .

Run the Docker container:
This will map port 8000 on your host machine to port 8000 inside the container.

docker run -p 8000:8000 translator-microservice

The API will then be accessible at http://localhost:8000.

Future Enhancements
Real Google Translate API Integration: Replace the mock/LLM engines with actual calls to the Google Cloud Translation API for production use.

Source Language Detection: Implement or integrate a robust source language detection library to automatically identify the source_language.

Advanced Configuration Management: Utilize pydantic-settings or similar libraries for more sophisticated management of environment variables and application settings.

CI/CD Pipeline: Set up automated testing and deployment workflows (e.g., using GitHub Actions, GitLab CI, Jenkins) to streamline development.

Database Migration Tool: Integrate a tool like Alembic for managing database schema changes in a version-controlled manner.

Monitoring and Alerting: Integrate with monitoring tools (e.g., Prometheus, Grafana) and set up alerts for service health and performance.

License
This project is open-source and available under the MIT License. See the LICENSE file in the repository for more details.



