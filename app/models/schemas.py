from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

class SingleTranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to translate")
    target_lang: str = Field(..., min_length=2, max_length=2, description="Target language code (ISO 639-1)")

    @validator('target_lang')
    def validate_language_code(cls, v):
        # ISO 639-1 language codes are 2 characters
        if not re.match(r'^[a-z]{2}$', v.lower()):
            raise ValueError('target_lang must be a valid ISO 639-1 language code (2 characters)')
        return v.lower()

class BulkTranslationRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=10, description="List of texts to translate")
    target_lang: str = Field(..., min_length=2, max_length=2, description="Target language code (ISO 639-1)")

    @validator('texts')
    def validate_texts(cls, v):
        for text in v:
            if len(text) > 1000:
                raise ValueError(f'Text "{text[:50]}..." exceeds 1000 character limit')
            if len(text) == 0:
                raise ValueError('Text cannot be empty')
        return v

    @validator('target_lang')
    def validate_language_code(cls, v):
        if not re.match(r'^[a-z]{2}$', v.lower()):
            raise ValueError('target_lang must be a valid ISO 639-1 language code (2 characters)')
        return v.lower()

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    target_lang: str

class BulkTranslationResponse(BaseModel):
    translations: List[TranslationResponse]

class HealthResponse(BaseModel):
    status: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None 