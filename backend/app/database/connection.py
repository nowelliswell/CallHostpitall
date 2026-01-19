import sqlite3
import json
from typing import Dict, List, Any
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "hospital_queue.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                poly TEXT NOT NULL,
                number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                called_at TIMESTAMP NULL,
                status TEXT DEFAULT 'waiting'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queue_numbers (
                poly TEXT PRIMARY KEY,
                current_number INTEGER DEFAULT 1
            )
        """)
        
        # Initialize poly numbers if not exists
        polies = ["Poli Umum", "Poli Gigi", "Poli Anak", "Poli Kandungan", "Pemeriksaan BPJS"]
        for poly in polies:
            cursor.execute(
                "INSERT OR IGNORE INTO queue_numbers (poly, current_number) VALUES (?, 1)",
                (poly,)
            )
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows

# Global database instance
db_manager = DatabaseManager()