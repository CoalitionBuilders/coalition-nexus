import pytest
import sqlite3
import os

class TestDatabase:
    def test_db_exists(self):
        db_files = [f for f in os.listdir('.') if f.endswith('.db') or f.endswith('.sqlite')]
        assert len(db_files) > 0, 'No database file found'
    
    def test_db_structure(self):
        db_files = [f for f in os.listdir('.') if f.endswith('.db') or f.endswith('.sqlite')]
        if db_files:
            conn = sqlite3.connect(db_files[0])
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            assert len(tables) > 0, 'Database has no tables'