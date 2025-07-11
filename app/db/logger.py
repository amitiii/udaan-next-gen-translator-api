import sqlite3

def init_db():
    conn = sqlite3.connect("translations.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original TEXT,
        translated TEXT,
        lang TEXT
    )
    """)
    conn.commit()
    conn.close()