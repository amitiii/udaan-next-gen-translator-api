
from app.adapters.mock_adapter import MockTranslator
from app.adapters.llm_adapter import LLMTranslator
from app.core.config import SUPPORTED_LANGUAGES
from app.db.logger import log_translation
from app.models.schemas import TranslationResponse

translator = MockTranslator()

async def translate_sentence(text: str, target_lang: str) -> TranslationResponse:
    if target_lang not in SUPPORTED_LANGUAGES:
        raise ValueError("Unsupported target language")
    translated = translator.translate(text, target_lang)
    log_translation(text, translated, target_lang)
    return TranslationResponse(original_text=text, translated_text=translated, target_lang=target_lang)
