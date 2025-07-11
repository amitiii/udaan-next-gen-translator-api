
import sqlite3

def init_db():
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original TEXT,
            translated TEXT,
            lang TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_translation(original, translated, lang):
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (original, translated, lang) VALUES (?, ?, ?)',
                   (original, translated, lang))
    conn.commit()
    conn.close()
