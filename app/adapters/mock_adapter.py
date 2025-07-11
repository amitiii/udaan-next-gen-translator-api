class MockTranslator:
    MOCK_DICT = {
        'hi': {'hello': 'नमस्ते', 'world': 'दुनिया'},
        'ta': {'hello': 'வணக்கம்', 'world': 'உலகம்'},
        'bn': {'hello': 'হ্যালো', 'world': 'বিশ্ব'},
        'kn': {'hello': 'ಹಲೋ', 'world': 'ವಿಶ್ವ'},
    }

    def translate(self, text: str, lang: str) -> str:
        return ' '.join([self.MOCK_DICT.get(lang, {}).get(word.lower(), word) for word in text.split()])