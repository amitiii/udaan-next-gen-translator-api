import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class TranslationLogger:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.getenv("TRANSLATION_DB_PATH", "translation_logs.db")
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create translation_logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS translation_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        input_text TEXT NOT NULL,
                        target_language TEXT NOT NULL,
                        translated_text TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT,
                        request_type TEXT DEFAULT 'single',
                        status TEXT DEFAULT 'success',
                        error_message TEXT,
                        processing_time_ms INTEGER
                    )
                ''')
                
                # Create bulk_translation_logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bulk_translation_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        request_id TEXT NOT NULL,
                        input_texts TEXT NOT NULL,
                        target_language TEXT NOT NULL,
                        translated_texts TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT,
                        status TEXT DEFAULT 'success',
                        error_message TEXT,
                        processing_time_ms INTEGER,
                        texts_count INTEGER
                    )
                ''')
                
                conn.commit()
                
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def log_single_translation(self, 
                             input_text: str, 
                             target_language: str, 
                             translated_text: Optional[str] = None,
                             ip_address: Optional[str] = None,
                             status: str = "success",
                             error_message: Optional[str] = None,
                             processing_time_ms: Optional[int] = None) -> int:
        """
        Log a single translation request.
        
        Args:
            input_text (str): Original input text
            target_language (str): Target language code
            translated_text (str, optional): Translated text
            ip_address (str, optional): Client IP address
            status (str): Request status (success/error)
            error_message (str, optional): Error message if failed
            processing_time_ms (int, optional): Processing time in milliseconds
            
        Returns:
            int: Log entry ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO translation_logs 
                    (input_text, target_language, translated_text, ip_address, status, error_message, processing_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (input_text, target_language, translated_text, ip_address, status, error_message, processing_time_ms))
                
                log_id = cursor.lastrowid
                conn.commit()
                return log_id
                
        except Exception as e:
            print(f"Error logging translation: {e}")
            return -1
    
    def log_bulk_translation(self,
                           request_id: str,
                           input_texts: List[str],
                           target_language: str,
                           translated_texts: Optional[List[str]] = None,
                           ip_address: Optional[str] = None,
                           status: str = "success",
                           error_message: Optional[str] = None,
                           processing_time_ms: Optional[int] = None) -> int:
        """
        Log a bulk translation request.
        
        Args:
            request_id (str): Unique request identifier
            input_texts (List[str]): List of input texts
            target_language (str): Target language code
            translated_texts (List[str], optional): List of translated texts
            ip_address (str, optional): Client IP address
            status (str): Request status (success/error)
            error_message (str, optional): Error message if failed
            processing_time_ms (int, optional): Processing time in milliseconds
            
        Returns:
            int: Log entry ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                input_texts_json = json.dumps(input_texts)
                translated_texts_json = json.dumps(translated_texts) if translated_texts else None
                
                cursor.execute('''
                    INSERT INTO bulk_translation_logs 
                    (request_id, input_texts, target_language, translated_texts, ip_address, status, error_message, processing_time_ms, texts_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (request_id, input_texts_json, target_language, translated_texts_json, ip_address, status, error_message, processing_time_ms, len(input_texts)))
                
                log_id = cursor.lastrowid
                conn.commit()
                return log_id
                
        except Exception as e:
            print(f"Error logging bulk translation: {e}")
            return -1
    
    def get_translation_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Get translation statistics for the last N days.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            Dict[str, Any]: Statistics including total requests, success rate, etc.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Single translation stats
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_requests,
                        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_requests,
                        AVG(processing_time_ms) as avg_processing_time
                    FROM translation_logs 
                    WHERE timestamp >= datetime('now', '-{} days')
                '''.format(days))
                
                single_stats = cursor.fetchone()
                
                # Bulk translation stats
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_requests,
                        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_requests,
                        AVG(processing_time_ms) as avg_processing_time,
                        SUM(texts_count) as total_texts_processed
                    FROM bulk_translation_logs 
                    WHERE timestamp >= datetime('now', '-{} days')
                '''.format(days))
                
                bulk_stats = cursor.fetchone()
                
                # Language usage stats
                cursor.execute('''
                    SELECT target_language, COUNT(*) as count
                    FROM translation_logs 
                    WHERE timestamp >= datetime('now', '-{} days')
                    GROUP BY target_language
                    ORDER BY count DESC
                    LIMIT 10
                '''.format(days))
                
                language_stats = cursor.fetchall()
                
                return {
                    "single_translations": {
                        "total_requests": single_stats[0] or 0,
                        "successful_requests": single_stats[1] or 0,
                        "success_rate": round((single_stats[1] or 0) / (single_stats[0] or 1) * 100, 2),
                        "avg_processing_time_ms": round(single_stats[2] or 0, 2)
                    },
                    "bulk_translations": {
                        "total_requests": bulk_stats[0] or 0,
                        "successful_requests": bulk_stats[1] or 0,
                        "success_rate": round((bulk_stats[1] or 0) / (bulk_stats[0] or 1) * 100, 2),
                        "avg_processing_time_ms": round(bulk_stats[2] or 0, 2),
                        "total_texts_processed": bulk_stats[3] or 0
                    },
                    "top_languages": [{"language": lang, "count": count} for lang, count in language_stats]
                }
                
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent translation logs.
        
        Args:
            limit (int): Number of recent logs to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of recent log entries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, input_text, target_language, translated_text, timestamp, ip_address, status, processing_time_ms
                    FROM translation_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                logs = []
                for row in cursor.fetchall():
                    logs.append({
                        "id": row[0],
                        "input_text": row[1],
                        "target_language": row[2],
                        "translated_text": row[3],
                        "timestamp": row[4],
                        "ip_address": row[5],
                        "status": row[6],
                        "processing_time_ms": row[7]
                    })
                
                return logs
                
        except Exception as e:
            print(f"Error getting recent logs: {e}")
            return []
    
    def cleanup_old_logs(self, days: int = 30):
        """
        Clean up logs older than specified days.
        
        Args:
            days (int): Number of days to keep logs
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    DELETE FROM translation_logs 
                    WHERE timestamp < datetime('now', '-{} days')
                '''.format(days))
                
                cursor.execute('''
                    DELETE FROM bulk_translation_logs 
                    WHERE timestamp < datetime('now', '-{} days')
                '''.format(days))
                
                conn.commit()
                
        except Exception as e:
            print(f"Error cleaning up logs: {e}") 