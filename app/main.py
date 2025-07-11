from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes.translate import router as translate_router
from app.models.schemas import ErrorResponse

# Load environment variables from .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translate_router, prefix="/api/v1", tags=["translation"])

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify service status.
    """
    return {"status": "healthy", "service": "translation-microservice"}

@app.get("/")
async def root():
    """
    Root endpoint with service information.
    """
    return {
        "service": "Translation Microservice",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "mock_translate": "/api/v1/translate/mock",
            "mock_bulk_translate": "/api/v1/translate/bulk/mock",
            "gemini_translate": "/api/v1/translate/gemini",
            "gemini_bulk_translate": "/api/v1/translate/bulk/gemini",
            "languages": "/api/v1/languages",
            "detect": "/api/v1/detect",
            "stats": "/api/v1/stats",
            "logs": "/api/v1/logs",
            "docs": "/docs"
        }
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and return consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=f"Request to {request.url.path} failed"
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions and return consistent error format."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    ) 