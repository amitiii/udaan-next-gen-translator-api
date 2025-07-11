from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import time
import uuid
from datetime import datetime

from app.models.schemas import (
    SingleTranslationRequest, 
    BulkTranslationRequest, 
    TranslationResponse, 
    BulkTranslationResponse,
    ErrorResponse
)
from app.services.translator import TranslationService
from app.services.gemini_translator import GeminiTranslator
from app.db.logger import TranslationLogger
from app.utils.validators import validate_language_code, sanitize_text

router = APIRouter()

# Initialize services
translation_service = TranslationService()
gemini_translator = GeminiTranslator()
logger = TranslationLogger()

def get_client_ip(request: Request) -> str:
    """Extract client IP address from request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

@router.post("/translate/mock", response_model=TranslationResponse)
async def translate_text_mock(
    request_data: SingleTranslationRequest,
    http_request: Request
):
    """
    Translate a single text to the target language.
    """
    start_time = time.time()
    client_ip = get_client_ip(http_request)
    
    try:
        # Sanitize input
        sanitized_text = sanitize_text(request_data.text)
        target_lang = request_data.target_lang.lower()
        
        # Get supported languages dynamically from API
        supported_languages = translation_service.get_supported_languages()
        
        # Validate language code against dynamic list
        if not validate_language_code(target_lang, supported_languages):
            if supported_languages:
                available_langs = ", ".join(list(supported_languages.keys())[:10])
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported language code: {target_lang}. Available languages: {available_langs}..."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Language validation failed. Please check the language code: {target_lang}"
                )
        
        # Perform translation
        result = translation_service.translate_text(sanitized_text, target_lang)
        
        if result["status"] == "error":
            # Log the error
            logger.log_single_translation(
                input_text=sanitized_text,
                target_language=target_lang,
                ip_address=client_ip,
                status="error",
                error_message=result["error_message"],
                processing_time_ms=result["processing_time_ms"]
            )
            
            raise HTTPException(
                status_code=500,
                detail=f"Translation failed: {result['error_message']}"
            )
        
        # Log successful translation
        logger.log_single_translation(
            input_text=sanitized_text,
            target_language=target_lang,
            translated_text=result["translated_text"],
            ip_address=client_ip,
            status="success",
            processing_time_ms=result["processing_time_ms"]
        )
        
        return TranslationResponse(
            original_text=result["original_text"],
            translated_text=result["translated_text"],
            target_lang=result["target_lang"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log unexpected error
        logger.log_single_translation(
            input_text=request_data.text,
            target_language=request_data.target_lang,
            ip_address=client_ip,
            status="error",
            error_message=str(e),
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/translate/bulk/mock", response_model=BulkTranslationResponse)
async def translate_bulk_mock(
    request_data: BulkTranslationRequest,
    http_request: Request
):
    """
    Translate multiple texts to the target language.
    """
    start_time = time.time()
    client_ip = get_client_ip(http_request)
    request_id = str(uuid.uuid4())
    
    try:
        # Sanitize inputs
        sanitized_texts = [sanitize_text(text) for text in request_data.texts]
        target_lang = request_data.target_lang.lower()
        
        # Get supported languages dynamically from API
        supported_languages = translation_service.get_supported_languages()
        
        # Validate language code against dynamic list
        if not validate_language_code(target_lang, supported_languages):
            if supported_languages:
                available_langs = ", ".join(list(supported_languages.keys())[:10])
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported language code: {target_lang}. Available languages: {available_langs}..."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Language validation failed. Please check the language code: {target_lang}"
                )
        
        # Perform bulk translation
        result = translation_service.translate_bulk(sanitized_texts, target_lang)
        
        # Create response objects
        translations = []
        for translation in result["translations"]:
            translations.append(TranslationResponse(
                original_text=translation["original_text"],
                translated_text=translation["translated_text"],
                target_lang=translation["target_lang"]
            ))
        
        # Log the bulk translation
        translated_texts = [t["translated_text"] for t in result["translations"]]
        logger.log_bulk_translation(
            request_id=request_id,
            input_texts=sanitized_texts,
            target_language=target_lang,
            translated_texts=translated_texts,
            ip_address=client_ip,
            status=result["status"],
            error_message=result["error_message"],
            processing_time_ms=result["processing_time_ms"]
        )
        
        # Return response with additional metadata
        response = BulkTranslationResponse(translations=translations)
        
        # Add metadata to response headers
        response_headers = {
            "X-Request-ID": request_id,
            "X-Total-Texts": str(result["total_texts"]),
            "X-Successful-Translations": str(result["successful_translations"]),
            "X-Processing-Time-MS": str(result["processing_time_ms"])
        }
        
        return JSONResponse(
            content=response.dict(),
            headers=response_headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log unexpected error
        logger.log_bulk_translation(
            request_id=request_id,
            input_texts=request_data.texts,
            target_language=request_data.target_lang,
            ip_address=client_ip,
            status="error",
            error_message=str(e),
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported languages dynamically from Google Translate API.
    """
    try:
        languages = translation_service.get_supported_languages()
        return {
            "languages": languages,
            "total_count": len(languages),
            "timestamp": datetime.now().isoformat(),
            "source": "Google Translate API" if languages else "No API available"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve supported languages: {str(e)}"
        )

@router.post("/detect")
async def detect_language(text: str):
    """
    Detect the language of the input text.
    """
    try:
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )
        
        result = translation_service.detect_language(text.strip())
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=f"Language detection failed: {result['error_message']}"
            )
        
        return {
            "text": text,
            "detected_language": result["detected_language"],
            "confidence": result["confidence"],
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/stats")
async def get_translation_stats(days: int = 7):
    """
    Get translation statistics for the last N days.
    """
    try:
        if days < 1 or days > 365:
            raise HTTPException(
                status_code=400,
                detail="Days parameter must be between 1 and 365"
            )
        
        stats = logger.get_translation_stats(days)
        return {
            "stats": stats,
            "period_days": days,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )

@router.get("/logs")
async def get_recent_logs(limit: int = 10):
    """
    Get recent translation logs.
    """
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail="Limit parameter must be between 1 and 100"
            )
        
        logs = logger.get_recent_logs(limit)
        return {
            "logs": logs,
            "total_count": len(logs),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve logs: {str(e)}"
        )

@router.post("/translate/gemini", response_model=TranslationResponse)
async def translate_text_gemini(
    request_data: SingleTranslationRequest,
    http_request: Request
):
    """
    Translate a single text using Gemini Flash LLM model.
    """
    start_time = time.time()
    client_ip = get_client_ip(http_request)
    
    try:
        # Sanitize input
        sanitized_text = sanitize_text(request_data.text)
        target_lang = request_data.target_lang.lower()
        
        # Get supported languages from Gemini
        supported_languages = gemini_translator.get_supported_languages()
        
        # Validate language code
        if not validate_language_code(target_lang, supported_languages):
            if supported_languages:
                available_langs = ", ".join(list(supported_languages.keys())[:10])
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported language code: {target_lang}. Available languages: {available_langs}..."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Language validation failed. Please check the language code: {target_lang}"
                )
        
        # Perform translation with Gemini
        result = gemini_translator.translate_text(sanitized_text, target_lang)
        
        if result["status"] == "error":
            # Log the error
            logger.log_single_translation(
                input_text=sanitized_text,
                target_language=target_lang,
                ip_address=client_ip,
                status="error",
                error_message=result["error_message"],
                processing_time_ms=result["processing_time_ms"]
            )
            
            raise HTTPException(
                status_code=500,
                detail=f"Gemini translation failed: {result['error_message']}"
            )
        
        # Log successful translation
        logger.log_single_translation(
            input_text=sanitized_text,
            target_language=target_lang,
            translated_text=result["translated_text"],
            ip_address=client_ip,
            status="success",
            processing_time_ms=result["processing_time_ms"]
        )
        
        return TranslationResponse(
            original_text=result["original_text"],
            translated_text=result["translated_text"],
            target_lang=result["target_lang"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log unexpected error
        logger.log_single_translation(
            input_text=request_data.text,
            target_language=request_data.target_lang,
            ip_address=client_ip,
            status="error",
            error_message=str(e),
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/translate/bulk/gemini", response_model=BulkTranslationResponse)
async def translate_bulk_gemini(
    request_data: BulkTranslationRequest,
    http_request: Request
):
    """
    Translate multiple texts using Gemini Flash LLM model.
    """
    start_time = time.time()
    client_ip = get_client_ip(http_request)
    request_id = str(uuid.uuid4())
    
    try:
        # Sanitize inputs
        sanitized_texts = [sanitize_text(text) for text in request_data.texts]
        target_lang = request_data.target_lang.lower()
        
        # Get supported languages from Gemini
        supported_languages = gemini_translator.get_supported_languages()
        
        # Validate language code
        if not validate_language_code(target_lang, supported_languages):
            if supported_languages:
                available_langs = ", ".join(list(supported_languages.keys())[:10])
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported language code: {target_lang}. Available languages: {available_langs}..."
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Language validation failed. Please check the language code: {target_lang}"
                )
        
        # Perform bulk translation with Gemini
        result = gemini_translator.translate_bulk(sanitized_texts, target_lang)
        
        # Create response objects
        translations = []
        for translation in result["translations"]:
            translations.append(TranslationResponse(
                original_text=translation["original_text"],
                translated_text=translation["translated_text"],
                target_lang=translation["target_lang"]
            ))
        
        # Log the bulk translation
        translated_texts = [t["translated_text"] for t in result["translations"]]
        logger.log_bulk_translation(
            request_id=request_id,
            input_texts=sanitized_texts,
            target_language=target_lang,
            translated_texts=translated_texts,
            ip_address=client_ip,
            status=result["status"],
            error_message=result["error_message"],
            processing_time_ms=result["processing_time_ms"]
        )
        
        # Return response with additional metadata
        response = BulkTranslationResponse(translations=translations)
        
        # Add metadata to response headers
        response_headers = {
            "X-Request-ID": request_id,
            "X-Total-Texts": str(result["total_texts"]),
            "X-Successful-Translations": str(result["successful_translations"]),
            "X-Processing-Time-MS": str(result["processing_time_ms"]),
            "X-Model": result.get("model", "gemini-1.5-flash")
        }
        
        return JSONResponse(
            content=response.dict(),
            headers=response_headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log unexpected error
        logger.log_bulk_translation(
            request_id=request_id,
            input_texts=request_data.texts,
            target_language=request_data.target_lang,
            ip_address=client_ip,
            status="error",
            error_message=str(e),
            processing_time_ms=int((time.time() - start_time) * 1000)
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

 