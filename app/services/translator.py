import os
import time
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

class TranslationService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY", None)
        self.use_mock = True  # Always use mock for now due to googletrans compatibility issues
        self.supported_languages_cache = None
        self.languages_cache_time = 0
        self.cache_duration = 3600  # Cache languages for 1 hour
        print("Using mock translation service (googletrans compatibility mode)")
    
    def fetch_supported_languages_from_api(self) -> Dict[str, str]:
        """
        Get supported languages for mock translation service.
        
        Returns:
            Dict[str, str]: Dictionary of language codes and names
        """
        # Return a comprehensive list of supported languages for mock service
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
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages for mock translation service.
        
        Returns:
            Dict[str, str]: Dictionary of language codes and names
        """
        current_time = time.time()
        
        # Check if cache is still valid
        if (self.supported_languages_cache and 
            current_time - self.languages_cache_time < self.cache_duration):
            return self.supported_languages_cache
        
        # Get languages from mock service
        languages = self.fetch_supported_languages_from_api()
        if languages:
            self.supported_languages_cache = languages
            self.languages_cache_time = current_time
        
        return languages
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate a single text to the target language.
        
        Args:
            text (str): Text to translate
            target_lang (str): Target language code
            source_lang (str): Source language code (default: auto-detect)
            
        Returns:
            Dict[str, Any]: Translation result with status and data
        """
        start_time = time.time()
        
        try:
            # Use mock translation service
            translated_text = self._mock_translate(text, target_lang)
            status = "success"
            error_message = None
                
        except Exception as e:
            translated_text = None
            status = "error"
            error_message = f"Translation failed: {str(e)}"
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_lang": target_lang,
            "status": status,
            "error_message": error_message,
            "processing_time_ms": processing_time_ms
        }
    
    def translate_bulk(self, texts: List[str], target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """
        Translate multiple texts to the target language.
        
        Args:
            texts (List[str]): List of texts to translate
            target_lang (str): Target language code
            source_lang (str): Source language code (default: auto-detect)
            
        Returns:
            Dict[str, Any]: Bulk translation result with status and data
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
            "successful_translations": len([t for t in translations if t["translated_text"] is not None])
        }
    
    def _mock_translate(self, text: str, target_lang: str) -> str:
        """
        Mock translation function with common phrase translations.
        
        Args:
            text (str): Text to translate
            target_lang (str): Target language code
            
        Returns:
            str: Mock translated text
        """
        # Common phrase translations for mock service
        common_translations = {
            'ta': {  # Tamil
                'hello': 'வணக்கம்',
                'how are you': 'நீங்கள் எப்படி இருக்கிறீர்கள்',
                'good morning': 'காலை வணக்கம்',
                'good evening': 'மாலை வணக்கம்',
                'thank you': 'நன்றி',
                'welcome': 'வரவேற்கிறேன்',
                'goodbye': 'பிரியாவிடை',
                'yes': 'ஆம்',
                'no': 'இல்லை',
                'please': 'தயவுசெய்து',
                'sorry': 'மன்னிக்கவும்',
                'excuse me': 'மன்னிக்கவும்',
                'what is your name': 'உங்கள் பெயர் என்ன',
                'my name is': 'என் பெயர்',
                'nice to meet you': 'உங்களை சந்தித்ததில் மகிழ்ச்சி',
                'where are you from': 'நீங்கள் எங்கிருந்து வருகிறீர்கள்',
                'i am from': 'நான் வருகிறேன்',
                'how old are you': 'உங்கள் வயது என்ன',
                'i am': 'நான்',
                'years old': 'வயது',
                'do you speak english': 'நீங்கள் ஆங்கிலம் பேசுகிறீர்களா',
                'i speak': 'நான் பேசுகிறேன்',
                'i understand': 'நான் புரிந்துகொள்கிறேன்',
                'i do not understand': 'நான் புரிந்துகொள்ளவில்லை',
                'can you help me': 'நீங்கள் எனக்கு உதவ முடியுமா',
                'where is': 'எங்கே உள்ளது',
                'how much': 'எவ்வளவு',
                'what time': 'என்ன நேரம்',
                'today': 'இன்று',
                'tomorrow': 'நாளை',
                'yesterday': 'நேற்று',
                'good': 'நல்லது',
                'bad': 'மோசமானது',
                'beautiful': 'அழகான',
                'big': 'பெரிய',
                'small': 'சிறிய',
                'hot': 'சூடான',
                'cold': 'குளிர்ந்த',
                'water': 'தண்ணீர்',
                'food': 'உணவு',
                'house': 'வீடு',
                'car': 'கார்',
                'book': 'புத்தகம்',
                'phone': 'தொலைபேசி',
                'computer': 'கணினி',
                'money': 'பணம்',
                'time': 'நேரம்',
                'day': 'நாள்',
                'night': 'இரவு',
                'morning': 'காலை',
                'evening': 'மாலை',
                'family': 'குடும்பம்',
                'friend': 'நண்பர்',
                'work': 'வேலை',
                'school': 'பள்ளி',
                'hospital': 'மருத்துவமனை',
                'market': 'சந்தை',
                'restaurant': 'உணவகம்',
                'hotel': 'விடுதி',
                'airport': 'விமான நிலையம்',
                'station': 'நிலையம்',
                'bank': 'வங்கி',
                'post office': 'அஞ்சலகம்',
                'police': 'காவல்துறை',
                'doctor': 'மருத்துவர்',
                'teacher': 'ஆசிரியர்',
                'student': 'மாணவர்',
                'engineer': 'பொறியாளர்',
                'business': 'வணிகம்',
                'government': 'அரசு',
                'country': 'நாடு',
                'city': 'நகரம்',
                'village': 'கிராமம்',
                'road': 'சாலை',
                'bridge': 'பாலம்',
                'river': 'ஆறு',
                'mountain': 'மலை',
                'sea': 'கடல்',
                'sun': 'சூரியன்',
                'moon': 'சந்திரன்',
                'star': 'நட்சத்திரம்',
                'rain': 'மழை',
                'snow': 'பனி',
                'wind': 'காற்று',
                'fire': 'நெருப்பு',
                'earth': 'பூமி',
                'sky': 'வானம்',
                'tree': 'மரம்',
                'flower': 'மலர்',
                'bird': 'பறவை',
                'fish': 'மீன்',
                'dog': 'நாய்',
                'cat': 'பூனை',
                'horse': 'குதிரை',
                'cow': 'பசு',
                'chicken': 'கோழி',
                'bread': 'ரொட்டி',
                'rice': 'அரிசி',
                'milk': 'பால்',
                'egg': 'முட்டை',
                'meat': 'இறைச்சி',
                'vegetable': 'காய்கறி',
                'fruit': 'பழம்',
                'coffee': 'காபி',
                'tea': 'தேநீர்',
                'juice': 'சாறு',
                'beer': 'பீர்',
                'wine': 'மது',
                'salt': 'உப்பு',
                'sugar': 'சர்க்கரை',
                'oil': 'எண்ணெய்',
                'butter': 'வெண்ணெய்',
                'cheese': 'பாலாடைக்கட்டி',
                'soup': 'சூப்',
                'salad': 'சாலட்',
                'cake': 'கேக்',
                'ice cream': 'ஐஸ் கிரீம்',
                'chocolate': 'சாக்லேட்',
                'candy': 'மிட்டாய்',
                'medicine': 'மருந்து',
                'pill': 'மாத்திரை',
                'bandage': 'கட்டு',
                'temperature': 'வெப்பநிலை',
                'fever': 'காய்ச்சல்',
                'headache': 'தலைவலி',
                'stomachache': 'வயிற்றுவலி',
                'toothache': 'பல்வலி',
                'cough': 'இருமல்',
                'cold': 'தடுப்பு',
                'flu': 'காய்ச்சல்',
                'allergy': 'ஒவ்வாமை',
                'diabetes': 'நீரிழிவு',
                'heart': 'இதயம்',
                'brain': 'மூளை',
                'eye': 'கண்',
                'ear': 'காது',
                'nose': 'மூக்கு',
                'mouth': 'வாய்',
                'hand': 'கை',
                'foot': 'கால்',
                'head': 'தலை',
                'hair': 'முடி',
                'skin': 'தோல்',
                'bone': 'எலும்பு',
                'blood': 'இரத்தம்',
                'muscle': 'தசை',
                'nerve': 'நரம்பு',
                'vein': 'சிரை',
                'artery': 'தமனி',
                'lung': 'நுரையீரல்',
                'liver': 'கல்லீரல்',
                'kidney': 'சிறுநீரகம்',
                'stomach': 'வயிறு',
                'intestine': 'குடல்',
                'bladder': 'சிறுநீர்ப்பை',
                'pancreas': 'கணையம்',
                'spleen': 'மண்ணீரல்',
                'gallbladder': 'பித்தப்பை',
                'appendix': 'குடல்வால்',
                'tonsil': 'டான்சில்',
                'adenoid': 'அடினாய்டு',
                'thyroid': 'தைராய்டு',
                'adrenal': 'அட்ரினல்',
                'pituitary': 'பிட்யூட்டரி',
                'pineal': 'பினியல்',
                'thymus': 'தைமஸ்',
                'ovary': 'கருப்பை',
                'testis': 'விரை',
                'uterus': 'கர்ப்பப்பை',
                'vagina': 'யோனி',
                'penis': 'ஆண்குறி',
                'breast': 'மார்பகம்',
                'nipple': 'முலைக்காம்பு',
                'navel': 'தொப்புள்',
                'belly button': 'தொப்புள்',
                'armpit': 'அக்குள்',
                'elbow': 'முழங்கை',
                'wrist': 'மணிக்கட்டு',
                'finger': 'விரல்',
                'thumb': 'கட்டைவிரல்',
                'index finger': 'சுட்டுவிரல்',
                'middle finger': 'நடுவிரல்',
                'ring finger': 'மோதிரவிரல்',
                'little finger': 'சிறுவிரல்',
                'toe': 'கால் விரல்',
                'big toe': 'கட்டைக்கால் விரல்',
                'ankle': 'கணுக்கால்',
                'knee': 'முழங்கால்',
                'thigh': 'துடை',
                'calf': 'கன்று',
                'shin': 'முன்கால்',
                'heel': 'குதிகால்',
                'sole': 'உள்ளங்கால்',
                'arch': 'வளைவு',
                'ball': 'பந்து',
                'joint': 'மூட்டு',
                'ligament': 'தசைநார்',
                'tendon': 'தசைநாண்',
                'cartilage': 'குருத்தெலும்பு',
                'marrow': 'எலும்பு மஜ்ஜை',
                'plasma': 'பிளாஸ்மா',
                'platelet': 'தட்டு',
                'white blood cell': 'வெள்ளை இரத்த அணு',
                'red blood cell': 'சிவப்பு இரத்த அணு',
                'hemoglobin': 'ஹீமோகுளோபின்',
                'oxygen': 'ஆக்சிஜன்',
                'carbon dioxide': 'கரியமில வாயு',
                'nitrogen': 'நைட்ரஜன்',
                'hydrogen': 'ஹைட்ரஜன்',
                'helium': 'ஹீலியம்',
                'neon': 'நியான்',
                'argon': 'ஆர்கான்',
                'krypton': 'கிரிப்டான்',
                'xenon': 'செனான்',
                'radon': 'ரேடான்',
                'lithium': 'லித்தியம்',
                'sodium': 'சோடியம்',
                'potassium': 'பொட்டாசியம்',
                'rubidium': 'ருபிடியம்',
                'cesium': 'சீசியம்',
                'francium': 'பிரான்சியம்',
                'beryllium': 'பெரிலியம்',
                'magnesium': 'மக்னீசியம்',
                'calcium': 'கால்சியம்',
                'strontium': 'ஸ்ட்ரான்சியம்',
                'barium': 'பேரியம்',
                'radium': 'ரேடியம்',
                'scandium': 'ஸ்காண்டியம்',
                'yttrium': 'இட்ரியம்',
                'lanthanum': 'லாந்தனம்',
                'actinium': 'அக்டினியம்',
                'titanium': 'டைட்டானியம்',
                'zirconium': 'சிர்கோனியம்',
                'hafnium': 'ஹாஃப்னியம்',
                'rutherfordium': 'ரதர்ஃபோர்டியம்',
                'vanadium': 'வனேடியம்',
                'niobium': 'நையோபியம்',
                'tantalum': 'டாண்டலம்',
                'dubnium': 'டுப்னியம்',
                'chromium': 'குரோமியம்',
                'molybdenum': 'மாலிப்டினம்',
                'tungsten': 'டங்ஸ்டன்',
                'seaborgium': 'சீபோர்கியம்',
                'manganese': 'மாங்கனீசு',
                'technetium': 'டெக்னீசியம்',
                'rhenium': 'ரீனியம்',
                'bohrium': 'போரியம்',
                'iron': 'இரும்பு',
                'ruthenium': 'ருடேனியம்',
                'osmium': 'ஒஸ்மியம்',
                'hassium': 'ஹாசியம்',
                'cobalt': 'கோபால்ட்',
                'rhodium': 'ரோடியம்',
                'iridium': 'இரிடியம்',
                'meitnerium': 'மெய்ட்னெரியம்',
                'nickel': 'நிக்கல்',
                'palladium': 'பல்லேடியம்',
                'platinum': 'பிளாட்டினம்',
                'darmstadtium': 'டார்ம்ஸ்டாடியம்',
                'copper': 'செம்பு',
                'silver': 'வெள்ளி',
                'gold': 'தங்கம்',
                'roentgenium': 'ரோன்ட்ஜெனியம்',
                'zinc': 'துத்தநாகம்',
                'cadmium': 'காட்மியம்',
                'mercury': 'பாதரசம்',
                'copernicium': 'கோப்பர்னிக்கியம்',
                'boron': 'போரான்',
                'aluminum': 'அலுமினியம்',
                'gallium': 'காலியம்',
                'indium': 'இண்டியம்',
                'thallium': 'தாலியம்',
                'nihonium': 'நிகோனியம்',
                'carbon': 'கரிமம்',
                'silicon': 'சிலிக்கான்',
                'germanium': 'ஜெர்மானியம்',
                'tin': 'தகரம்',
                'lead': 'ஈயம்',
                'flerovium': 'ஃப்ளெரோவியம்',
                'nitrogen': 'நைட்ரஜன்',
                'phosphorus': 'பாஸ்பரஸ்',
                'arsenic': 'ஆர்சனிக்',
                'antimony': 'ஆண்டிமனி',
                'bismuth': 'பிஸ்மத்',
                'moscovium': 'மாஸ்கோவியம்',
                'oxygen': 'ஆக்சிஜன்',
                'sulfur': 'கந்தகம்',
                'selenium': 'செலினியம்',
                'tellurium': 'டெல்லூரியம்',
                'polonium': 'போலோனியம்',
                'livermorium': 'லிவர்மோரியம்',
                'fluorine': 'ஃப்ளூரின்',
                'chlorine': 'குளோரின்',
                'bromine': 'புரோமின்',
                'iodine': 'அயோடின்',
                'astatine': 'அஸ்டடின்',
                'tennessine': 'டென்னெசின்',
                'helium': 'ஹீலியம்',
                'neon': 'நியான்',
                'argon': 'ஆர்கான்',
                'krypton': 'கிரிப்டான்',
                'xenon': 'செனான்',
                'radon': 'ரேடான்',
                'oganesson': 'ஒகனெசான்'
            },
            'hi': {  # Hindi
                'hello': 'नमस्ते',
                'how are you': 'आप कैसे हैं',
                'good morning': 'सुप्रभात',
                'good evening': 'शुभ संध्या',
                'thank you': 'धन्यवाद',
                'welcome': 'स्वागत है',
                'goodbye': 'अलविदा',
                'yes': 'हाँ',
                'no': 'नहीं',
                'please': 'कृपया',
                'sorry': 'माफ़ कीजिए',
                'excuse me': 'माफ़ कीजिए',
                'what is your name': 'आपका नाम क्या है',
                'my name is': 'मेरा नाम है',
                'nice to meet you': 'आपसे मिलकर खुशी हुई',
                'where are you from': 'आप कहाँ से हैं',
                'i am from': 'मैं से हूँ',
                'how old are you': 'आपकी उम्र क्या है',
                'i am': 'मैं हूँ',
                'years old': 'साल का',
                'do you speak english': 'क्या आप अंग्रेज़ी बोलते हैं',
                'i speak': 'मैं बोलता हूँ',
                'i understand': 'मैं समझता हूँ',
                'i do not understand': 'मैं नहीं समझता',
                'can you help me': 'क्या आप मेरी मदद कर सकते हैं',
                'where is': 'कहाँ है',
                'how much': 'कितना',
                'what time': 'क्या समय है',
                'today': 'आज',
                'tomorrow': 'कल',
                'yesterday': 'कल',
                'good': 'अच्छा',
                'bad': 'बुरा',
                'beautiful': 'सुंदर',
                'big': 'बड़ा',
                'small': 'छोटा',
                'hot': 'गरम',
                'cold': 'ठंडा',
                'water': 'पानी',
                'food': 'खाना',
                'house': 'घर',
                'car': 'कार',
                'book': 'किताब',
                'phone': 'फ़ोन',
                'computer': 'कंप्यूटर',
                'money': 'पैसा',
                'time': 'समय',
                'day': 'दिन',
                'night': 'रात',
                'morning': 'सुबह',
                'evening': 'शाम',
                'family': 'परिवार',
                'friend': 'दोस्त',
                'work': 'काम',
                'school': 'स्कूल',
                'hospital': 'अस्पताल',
                'market': 'बाज़ार',
                'restaurant': 'रेस्तरां',
                'hotel': 'होटल',
                'airport': 'हवाई अड्डा',
                'station': 'स्टेशन',
                'bank': 'बैंक',
                'post office': 'डाकघर',
                'police': 'पुलिस',
                'doctor': 'डॉक्टर',
                'teacher': 'शिक्षक',
                'student': 'छात्र',
                'engineer': 'इंजीनियर',
                'business': 'व्यवसाय',
                'government': 'सरकार',
                'country': 'देश',
                'city': 'शहर',
                'village': 'गाँव',
                'road': 'सड़क',
                'bridge': 'पुल',
                'river': 'नदी',
                'mountain': 'पहाड़',
                'sea': 'समुद्र',
                'sun': 'सूरज',
                'moon': 'चाँद',
                'star': 'तारा',
                'rain': 'बारिश',
                'snow': 'बर्फ़',
                'wind': 'हवा',
                'fire': 'आग',
                'earth': 'पृथ्वी',
                'sky': 'आसमान',
                'tree': 'पेड़',
                'flower': 'फूल',
                'bird': 'पक्षी',
                'fish': 'मछली',
                'dog': 'कुत्ता',
                'cat': 'बिल्ली',
                'horse': 'घोड़ा',
                'cow': 'गाय',
                'chicken': 'मुर्गी',
                'bread': 'रोटी',
                'rice': 'चावल',
                'milk': 'दूध',
                'egg': 'अंडा',
                'meat': 'मांस',
                'vegetable': 'सब्ज़ी',
                'fruit': 'फल',
                'coffee': 'कॉफ़ी',
                'tea': 'चाय',
                'juice': 'जूस',
                'beer': 'बीयर',
                'wine': 'शराब',
                'salt': 'नमक',
                'sugar': 'चीनी',
                'oil': 'तेल',
                'butter': 'मक्खन',
                'cheese': 'पनीर',
                'soup': 'सूप',
                'salad': 'सलाद',
                'cake': 'केक',
                'ice cream': 'आइसक्रीम',
                'chocolate': 'चॉकलेट',
                'candy': 'कैंडी',
                'medicine': 'दवा',
                'pill': 'गोली',
                'bandage': 'पट्टी',
                'temperature': 'तापमान',
                'fever': 'बुखार',
                'headache': 'सिरदर्द',
                'stomachache': 'पेटदर्द',
                'toothache': 'दाँतदर्द',
                'cough': 'खाँसी',
                'cold': 'ज़ुकाम',
                'flu': 'फ्लू',
                'allergy': 'एलर्जी',
                'diabetes': 'मधुमेह',
                'heart': 'दिल',
                'brain': 'दिमाग',
                'eye': 'आँख',
                'ear': 'कान',
                'nose': 'नाक',
                'mouth': 'मुँह',
                'hand': 'हाथ',
                'foot': 'पैर',
                'head': 'सिर',
                'hair': 'बाल',
                'skin': 'त्वचा',
                'bone': 'हड्डी',
                'blood': 'खून',
                'muscle': 'मांसपेशी',
                'nerve': 'नस',
                'vein': 'शिरा',
                'artery': 'धमनी',
                'lung': 'फेफड़ा',
                'liver': 'जिगर',
                'kidney': 'गुर्दा',
                'stomach': 'पेट',
                'intestine': 'आंत',
                'bladder': 'मूत्राशय',
                'pancreas': 'अग्न्याशय',
                'spleen': 'तिल्ली',
                'gallbladder': 'पित्ताशय',
                'appendix': 'अपेंडिक्स',
                'tonsil': 'टॉन्सिल',
                'adenoid': 'एडेनॉइड',
                'thyroid': 'थायरॉइड',
                'adrenal': 'एड्रेनल',
                'pituitary': 'पिट्यूटरी',
                'pineal': 'पीनियल',
                'thymus': 'थाइमस',
                'ovary': 'अंडाशय',
                'testis': 'वृषण',
                'uterus': 'गर्भाशय',
                'vagina': 'योनि',
                'penis': 'लिंग',
                'breast': 'स्तन',
                'nipple': 'स्तनाग्र',
                'navel': 'नाभि',
                'belly button': 'नाभि',
                'armpit': 'बगल',
                'elbow': 'कोहनी',
                'wrist': 'कलाई',
                'finger': 'उंगली',
                'thumb': 'अंगूठा',
                'index finger': 'तर्जनी',
                'middle finger': 'मध्यमा',
                'ring finger': 'अनामिका',
                'little finger': 'कनिष्ठा',
                'toe': 'पैर की उंगली',
                'big toe': 'अंगूठा',
                'ankle': 'टखना',
                'knee': 'घुटना',
                'thigh': 'जाँघ',
                'calf': 'पिंडली',
                'shin': 'पिंडली',
                'heel': 'एड़ी',
                'sole': 'तलवा',
                'arch': 'मेहराब',
                'ball': 'गेंद',
                'joint': 'जोड़',
                'ligament': 'स्नायु',
                'tendon': 'कंडरा',
                'cartilage': 'उपास्थि',
                'marrow': 'मज्जा',
                'plasma': 'प्लाज्मा',
                'platelet': 'प्लेटलेट',
                'white blood cell': 'श्वेत रक्त कोशिका',
                'red blood cell': 'लाल रक्त कोशिका',
                'hemoglobin': 'हीमोग्लोबिन',
                'oxygen': 'ऑक्सीजन',
                'carbon dioxide': 'कार्बन डाइऑक्साइड',
                'nitrogen': 'नाइट्रोजन',
                'hydrogen': 'हाइड्रोजन',
                'helium': 'हीलियम',
                'neon': 'नियॉन',
                'argon': 'आर्गन',
                'krypton': 'क्रिप्टन',
                'xenon': 'ज़ेनॉन',
                'radon': 'रेडॉन',
                'oganesson': 'ओगनेसन'
            }
        }
        
        # Get translations for the target language
        translations = common_translations.get(target_lang, {})
        
        # Convert text to lowercase for matching
        text_lower = text.lower().strip()
        
        # Try to find exact match first
        if text_lower in translations:
            return translations[text_lower]
        
        # Try to find partial matches for common phrases (longest first)
        sorted_phrases = sorted(translations.keys(), key=len, reverse=True)
        
        result_text = text_lower
        for english_phrase in sorted_phrases:
            if english_phrase in result_text:
                # Replace the English phrase with translation
                result_text = result_text.replace(english_phrase, translations[english_phrase])
        
        # If we found any translations, return the result
        if result_text != text_lower:
            # Capitalize first letter and preserve original punctuation
            original_punctuation = text[-1] if text and text[-1] in '.,!?' else ''
            result_text = result_text.capitalize() + original_punctuation
            return result_text
        
        # If no match found, return with language suffix as fallback
        mock_suffixes = {
            'ta': ' (தமிழில்)',
            'hi': ' (हिंदी में)',
            'te': ' (తెలుగులో)',
            'bn': ' (বাংলায়)',
            'ur': ' (اردو میں)',
            'es': ' (en español)',
            'fr': ' (en français)',
            'de': ' (auf Deutsch)',
            'ja': ' (日本語で)',
            'ko': ' (한국어로)',
            'zh': ' (用中文)',
            'ar': ' (بالعربية)',
            'ru': ' (на русском)',
            'it': ' (in italiano)',
            'pt': ' (em português)',
            'nl': ' (in het Nederlands)',
            'sv': ' (på svenska)',
            'no': ' (på norsk)',
            'da': ' (på dansk)',
            'fi': ' (suomeksi)',
            'pl': ' (po polsku)',
            'tr': ' (Türkçe)',
            'he': ' (בעברית)',
            'id': ' (dalam bahasa Indonesia)',
            'ms': ' (dalam bahasa Melayu)',
            'fa': ' (به فارسی)',
            'uk': ' (українською)',
            'cs': ' (česky)',
            'sk': ' (slovensky)',
            'hu': ' (magyarul)',
            'ro': ' (în română)',
            'bg': ' (на български)',
            'hr': ' (na hrvatskom)',
            'sr': ' (на српском)',
            'sl': ' (v slovenščini)',
            'et': ' (eesti keeles)',
            'lv': ' (latviešu valodā)',
            'lt': ' (lietuvių kalba)',
            'el': ' (στα ελληνικά)',
            'is': ' (á íslensku)',
            'mt': ' (bil-Malti)',
            'ga': ' (as Gaeilge)',
            'cy': ' (yn Gymraeg)',
            'eu': ' (euskaraz)',
            'ca': ' (en català)',
            'gl': ' (en galego)',
            'af': ' (in Afrikaans)',
            'sw': ' (kwa Kiswahili)',
            'zu': ' (ngeZulu)',
            'xh': ' (ngeXhosa)',
            'st': ' (ka Sesotho)',
            'tn': ' (ka Setswana)',
            'ss': ' (ngeSiswati)',
            've': ' (tshiTshivenda)',
            'ts': ' (xiTsonga)',
            'nr': ' (isiNdebele)',
            'nd': ' (isiNdebele)',
            'th': ' (เป็นภาษาไทย)',
            'vi': ' (bằng tiếng Việt)'
        }
        
        suffix = mock_suffixes.get(target_lang, f' (in {target_lang})')
        return f"{text}{suffix}"
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the input text.
        
        Args:
            text (str): Text to detect language for
            
        Returns:
            Dict[str, Any]: Language detection result
        """
        try:
            # Simple mock language detection
            return {
                "detected_language": "en",
                "confidence": 0.8,
                "status": "success"
            }
        except Exception as e:
            return {
                "detected_language": None,
                "confidence": 0.0,
                "status": "error",
                "error_message": str(e)
            } 