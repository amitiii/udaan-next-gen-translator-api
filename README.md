# 🕊️ Udaan Next-Gen – Translation Microservice

🚀 An advanced, modular, production-ready **FastAPI-based translation microservice** built for the IIT Bombay AI Engineer Research Internship.

---

## 🔍 Overview

This microservice accepts input text and a target language, translates the content using a **mock dictionary** (or plug-in LLM model like Groq or Google Translate), and returns the translated result. Designed with extensibility, modularity, and performance in mind.

> ✅ **Bonus Features**: Async bulk translation, SQLite logging, health check, Docker deployment, plug-and-play translator adapter, and test-ready structure.

---
# Translation Microservice - Project Udaan

This project implements a lightweight, modular translation microservice using FastAPI. It provides a RESTful API to translate text, supports bulk translations, includes robust input validation, comprehensive error handling, and logs all translation requests to an SQLite database. The service is designed with a pluggable translation engine architecture, making it highly maintainable, scalable, and adaptable for integration into larger frameworks.

## Table of Contents

* [Features](#features)

* [Project Structure](#project-structure)

* [Setup and Installation](#setup-and-installation)

* [Running the Application](#running-the-application)

* [API Endpoints](#api-endpoints)

  * [`GET /health`](#get-health)

  * [`POST /api/v1/translate`](#post-apiv1translate)

  * [`POST /api/v1/bulk-translate`](#post-apiv1bulk-translate)

* [Pluggable Translation Engines](#pluggable-translation-engines)

* [Database Logging](#database-logging)

* [Running Tests](#running-tests)

* [Deployment](#deployment)

* [Future Enhancements](#future-enhancements)

* [License](#license)

## Features

* **FastAPI Framework**: High-performance, easy-to-use API development with automatic OpenAPI documentation.

* **Modular Architecture**: Clear separation of concerns (API, core logic, database, models, plugins) for enhanced maintainability.

* **Pluggable Translation Engines**: Easily switch between a Mock engine, an LLM-based engine, or integrate a real Google Translate API.

* **Robust Input Validation**: Utilizes Pydantic models for strict request and response schema validation, ensuring data integrity.

* **Comprehensive Logging**: Persists all translation requests and their responses to an SQLite database for auditing and analysis.

* **Health Check Endpoint**: A dedicated `/health` endpoint for quick service status monitoring.

* **Bulk Translation Support**: Efficiently translates multiple texts in a single API request.

* **Asynchronous Operations**: Leverages FastAPI's `async`/`await` capabilities for non-blocking I/O, improving concurrency and performance.

* **Automated API Documentation**: Self-generating interactive API documentation (Swagger UI) at `/docs` and ReDoc at `/redoc`.

* **Containerization Ready**: Includes a `Dockerfile` for seamless building and deployment in containerized environments.

* **Unit Tests**: Comprehensive test suite using `pytest` to ensure reliability and correctness of the application logic.

## Project Structure

├── app/
│   ├── api/                    # Defines FastAPI routes and endpoints
│   │   ├── init.py
│   │   └── v1/                 # Versioned API endpoints
│   │       ├── init.py
│   │       └── endpoints.py    # Main API endpoints (translate, bulk-translate, health)
│   ├── core/                   # Core application logic and configurations
│   │   ├── init.py
│   │   ├── config.py           # Application settings and configurations
│   │   └── translation_engine.py # Abstract base class for translation engines
│   ├── db/                     # Database setup and operations
│   │   ├── init.py
│   │   └── database.py         # SQLite database connection and logging functions
│   ├── models/                 # Pydantic models for request/response schemas
│   │   ├── init.py
│   │   └── schemas.py          # Defines data structures for API interactions
│   ├── plugins/                # Pluggable translation engine implementations
│   │   ├── init.py
│   │   ├── llm_engine.py       # LLM-based translation engine (example)
│   │   └── mock_engine.py      # Mock translation engine (default for demo)
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Unit and integration tests
│   ├── init.py
│   └── test_api.py             # Tests for API endpoints
├── Dockerfile                  # Docker build instructions
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
