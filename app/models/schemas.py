from pydantic import BaseModel, constr
from typing import List

class TranslateRequest(BaseModel):
    text: constr(min_length=1, max_length=1000)
    target_lang: constr(min_length=2, max_length=2)

class BulkRequest(BaseModel):
    sentences: List[TranslateRequest]

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    target_lang: str