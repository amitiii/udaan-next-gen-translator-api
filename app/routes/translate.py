
from fastapi import APIRouter, HTTPException
from app.models.schemas import TranslationRequest, BulkRequest, TranslationResponse
from app.services.translator import translate_sentence
from app.core.config import VERSION, SUPPORTED_LANGUAGES
import time, asyncio

router = APIRouter()

start_time = time.time()

@router.get("/health")
def health_check():
    uptime = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
    return {"status": "ok", "version": VERSION, "uptime": uptime, "language_support": SUPPORTED_LANGUAGES}

@router.post("/translate", response_model=TranslationResponse)
async def translate(req: TranslationRequest):
    return await translate_sentence(req.text, req.target_lang)

@router.post("/translate/bulk", response_model=list[TranslationResponse])
async def bulk_translate(req: BulkRequest):
    tasks = [translate_sentence(sentence.text, sentence.target_lang) for sentence in req.sentences]
    return await asyncio.gather(*tasks)
