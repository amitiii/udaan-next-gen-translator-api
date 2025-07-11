import os
import time
import google.generativeai as genai
from typing import Dict, Any, List
from dotenv import load_dotenv

class GeminiTranslator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.init_gemini()
    
    def init_gemini(self):
        """Initialize the Gemini model."""
        try:
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("Gemini 1.5 Flash model initialized successfully")
            
        except Exception as e:
            print(f"Gemini initialization failed: {e}")
            self.model = None
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate text using Gemini Flash model.
        
        Args:
            text (str): Text to translate
            target_lang (str): Target language code
            source_lang (str): Source language code (default: auto-detect)
            
        Returns:
            Dict[str, Any]: Translation result
        """
        start_time = time.time()
        
        try:
            if not self.model:
                raise Exception("Gemini model not initialized")
            
            # Create translation prompt with specific language mapping
            language_names = {
                'ta': 'Tamil',
                'hi': 'Hindi',
                'te': 'Telugu',
                'bn': 'Bengali',
                'ur': 'Urdu',
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
            
            target_language_name = language_names.get(target_lang, target_lang.upper())
            
            prompt = f"""
            Translate the following text to {target_language_name} language (ISO code: {target_lang}).
            Provide only the translated text without any explanations, quotes, or additional text.
            Make sure to translate to the correct language - {target_language_name} ({target_lang}).
            
            Text to translate: "{text}"
            
            Translated text:"""
            
            # Generate translation
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            # Remove quotes if present
            if translated_text.startswith('"') and translated_text.endswith('"'):
                translated_text = translated_text[1:-1]
            
            status = "success"
            error_message = None
            
        except Exception as e:
            translated_text = None
            status = "error"
            error_message = f"Gemini translation failed: {str(e)}"
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_lang": target_lang,
            "status": status,
            "error_message": error_message,
            "processing_time_ms": processing_time_ms,
            "model": "gemini-1.5-flash"
        }
    
    def translate_bulk(self, texts: List[str], target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate multiple texts using Gemini Flash model.
        
        Args:
            texts (List[str]): List of texts to translate
            target_lang (str): Target language code
            source_lang (str): Source language code (default: auto-detect)
            
        Returns:
            Dict[str, Any]: Bulk translation result
        """
        start_time = time.time()
        translations = []
        errors = []
        
        for i, text in enumerate(texts):
            try:
                result = self.translate_text(text, target_lang, source_lang)
                if result["status"] == "success":
                    translations.append({
                        "original_text": text,
                        "translated_text": result["translated_text"],
                        "target_lang": target_lang
                    })
                else:
                    errors.append(f"Text {i+1}: {result['error_message']}")
                    translations.append({
                        "original_text": text,
                        "translated_text": None,
                        "target_lang": target_lang
                    })
            except Exception as e:
                errors.append(f"Text {i+1}: {str(e)}")
                translations.append({
                    "original_text": text,
                    "translated_text": None,
                    "target_lang": target_lang
                })
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "translations": translations,
            "status": "success" if not errors else "partial_success",
            "error_message": "; ".join(errors) if errors else None,
            "processing_time_ms": processing_time_ms,
            "total_texts": len(texts),
            "successful_translations": len([t for t in translations if t["translated_text"] is not None]),
            "model": "gemini-1.5-flash"
        }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the input text using Gemini.
        
        Args:
            text (str): Text to detect language for
            
        Returns:
            Dict[str, Any]: Language detection result
        """
        try:
            if not self.model:
                raise Exception("Gemini model not initialized")
            
            prompt = f"""
            Detect the language of the following text and respond with only the ISO 639-1 language code (2 letters).
            If you cannot detect the language, respond with 'unknown'.
            
            Text: "{text}"
            
            Language code:"""
            
            response = self.model.generate_content(prompt)
            detected_language = response.text.strip().lower()
            
            # Validate language code format
            if len(detected_language) == 2 and detected_language.isalpha():
                return {
                    "detected_language": detected_language,
                    "confidence": 0.9,
                    "status": "success",
                    "model": "gemini-1.5-flash"
                }
            else:
                return {
                    "detected_language": "unknown",
                    "confidence": 0.0,
                    "status": "success",
                    "model": "gemini-1.5-flash"
                }
                
        except Exception as e:
            return {
                "detected_language": None,
                "confidence": 0.0,
                "status": "error",
                "error_message": str(e),
                "model": "gemini-1.5-flash"
            }
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages for Gemini translation.
        
        Returns:
            Dict[str, str]: Dictionary of language codes and names
        """
        return {
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