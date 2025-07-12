# 🌐 Translation Microservice - Project Udaan

This project implements a lightweight, modular translation microservice using FastAPI. It provides a RESTful API to translate text, supports bulk translations, includes robust input validation, comprehensive error handling, and logs all translation requests to an SQLite database.

The service is designed with a **pluggable translation engine architecture**, making it highly maintainable, scalable, and adaptable for integration into larger frameworks.

---

## 📚 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [`GET /health`](#get-health)
  - [`POST /api/v1/translate`](#post-apiv1translate)
  - [`POST /api/v1/bulk-translate`](#post-apiv1bulk-translate)
- [Pluggable Translation Engines](#pluggable-translation-engines)
- [Database Logging](#database-logging)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🚀 Features

- **FastAPI Framework**: High-performance, easy-to-use API development with automatic OpenAPI documentation.
- **Modular Architecture**: Clear separation of concerns (API, core logic, database, models, plugins) for enhanced maintainability.
- **Pluggable Translation Engines**: Easily switch between a Mock engine, an LLM-based engine, or integrate a real Google Translate API.
- **Robust Input Validation**: Utilizes Pydantic models for strict request/response validation.
- **Comprehensive Logging**: Persists all translation requests and their responses to an SQLite database.
- **Health Check Endpoint**: A dedicated `/health` endpoint for quick service monitoring.
- **Bulk Translation Support**: Efficiently translates multiple texts in a single request.
- **Asynchronous Operations**: FastAPI’s `async/await` for non-blocking I/O.
- **Automated API Documentation**: Swagger UI (`/docs`) and ReDoc (`/redoc`) available out of the box.
- **Containerization Ready**: Includes a `Dockerfile` for deployment.
- **Unit Tests**: Full coverage using `pytest`.

---

## 🗂️ Project Structure

```text
.
├── app/
│   ├── api/                    # FastAPI routes and endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints.py    # /translate, /bulk-translate, /health
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Settings and configs
│   │   └── translation_engine.py # Abstract engine base
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py         # SQLite logic and logging
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic request/response schemas
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── llm_engine.py       # LLM-based translation engine
│   │   └── mock_engine.py      # Mock engine for demo/testing
│   └── main.py                 # FastAPI app entry point
├── tests/
│   ├── __init__.py
│   └── test_api.py             # API tests
├── Dockerfile
├── requirements.txt
└── README.md

---

⚙️ Setup and Installation
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/amitiii/udaan-next-gen-translator-api.git
cd udaan-next-gen-translator-api
