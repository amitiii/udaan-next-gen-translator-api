from app.adapters.mock_adapter import MockTranslator
from app.adapters.llm_adapter import LLMTranslator

def get_translator(mode="mock"):
    return MockTranslator() if mode == "mock" else LLMTranslator()