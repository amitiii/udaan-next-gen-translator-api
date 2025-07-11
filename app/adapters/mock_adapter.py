
class MockTranslator:
    mock_dict = {
        'hi': {'hello': 'नमस्ते', 'world': 'दुनिया'},
        'ta': {'hello': 'வணக்கம்', 'world': 'உலகம்'},
        'bn': {'hello': 'হ্যালো', 'world': 'বিশ্ব'},
        'kn': {'hello': 'ಹಲೋ', 'world': 'ವಿಶ್ವ'},
    }

    def translate(self, text: str, lang: str) -> str:
        words = text.lower().split()
        translated = [self.mock_dict.get(lang, {}).get(w, w) for w in words]
        return ' '.join(translated)
