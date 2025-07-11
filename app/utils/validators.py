import re
from typing import List, Dict, Any

# Common ISO 639-1 language codes
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'bn': 'Bengali',
    'ur': 'Urdu',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish',
    'pl': 'Polish',
    'tr': 'Turkish',
    'he': 'Hebrew',
    'id': 'Indonesian',
    'ms': 'Malay',
    'fa': 'Persian',
    'uk': 'Ukrainian',
    'cs': 'Czech',
    'sk': 'Slovak',
    'hu': 'Hungarian',
    'ro': 'Romanian',
    'bg': 'Bulgarian',
    'hr': 'Croatian',
    'sr': 'Serbian',
    'sl': 'Slovenian',
    'et': 'Estonian',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'el': 'Greek',
    'is': 'Icelandic',
    'mt': 'Maltese',
    'ga': 'Irish',
    'cy': 'Welsh',
    'eu': 'Basque',
    'ca': 'Catalan',
    'gl': 'Galician',
    'af': 'Afrikaans',
    'sw': 'Swahili',
    'zu': 'Zulu',
    'xh': 'Xhosa',
    'st': 'Southern Sotho',
    'tn': 'Tswana',
    'ss': 'Swati',
    've': 'Venda',
    'ts': 'Tsonga',
    'nr': 'Southern Ndebele',
    'nd': 'Northern Ndebele'
}

def validate_language_code(lang_code: str, supported_languages: Dict[str, str] = None) -> bool:
    """
    Validate if the language code is a supported ISO 639-1 code.
    
    Args:
        lang_code (str): The language code to validate
        supported_languages (Dict[str, str], optional): Dynamic list of supported languages
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(lang_code, str):
        return False
    
    # Check if it's a 2-character code
    if not re.match(r'^[a-z]{2}$', lang_code.lower()):
        return False
    
    # If dynamic languages provided, check against that list
    if supported_languages:
        return lang_code.lower() in supported_languages
    
    # Fallback to static list
    return lang_code.lower() in SUPPORTED_LANGUAGES

def validate_text_length(text: str, max_length: int = 1000) -> bool:
    """
    Validate if text length is within limits.
    
    Args:
        text (str): The text to validate
        max_length (int): Maximum allowed length
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(text, str):
        return False
    
    return 1 <= len(text) <= max_length

def validate_bulk_texts(texts: List[str], max_length: int = 1000, max_items: int = 10) -> Dict[str, Any]:
    """
    Validate a list of texts for bulk translation.
    
    Args:
        texts (List[str]): List of texts to validate
        max_length (int): Maximum length per text
        max_items (int): Maximum number of texts
        
    Returns:
        Dict[str, Any]: Validation result with success flag and any errors
    """
    if not isinstance(texts, list):
        return {"valid": False, "error": "texts must be a list"}
    
    if len(texts) == 0:
        return {"valid": False, "error": "texts list cannot be empty"}
    
    if len(texts) > max_items:
        return {"valid": False, "error": f"Maximum {max_items} texts allowed per request"}
    
    for i, text in enumerate(texts):
        if not validate_text_length(text, max_length):
            return {
                "valid": False, 
                "error": f"Text at index {i} exceeds {max_length} character limit or is invalid"
            }
    
    return {"valid": True}

def get_supported_languages() -> Dict[str, str]:
    """
    Get the list of supported languages.
    
    Returns:
        Dict[str, str]: Dictionary of language codes and their names
    """
    return SUPPORTED_LANGUAGES.copy()

def sanitize_text(text: str) -> str:
    """
    Sanitize input text by removing extra whitespace.
    
    Args:
        text (str): Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        return ""
    
    return text.strip() 