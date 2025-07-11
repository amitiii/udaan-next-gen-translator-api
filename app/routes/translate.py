from fastapi import APIRouter, HTTPException
from app.models.schemas import TranslateRequest, BulkRequest, TranslationResponse
from app.services.translator import get_translator
from typing import List

router = APIRouter()

@router.post("/translate", response_model=TranslationResponse)
async def translate(payload: TranslateRequest):
    translator = get_translator()
    result = translator.translate(payload.text, payload.target_lang)
    return TranslationResponse(original_text=payload.text, translated_text=result, target_lang=payload.target_lang)

@router.post("/translate/bulk", response_model=List[TranslationResponse])
async def bulk_translate(payload: BulkRequest):
    translator = get_translator()
    return [
        TranslationResponse(
            original_text=req.text,
            translated_text=translator.translate(req.text, req.target_lang),
            target_lang=req.target_lang,
        ) for req in payload.sentences
    ]

@router.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0"}