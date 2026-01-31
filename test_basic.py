import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestBasicFunctionality(unittest.TestCase):
    def test_app_import(self):
        """Test that main app can be imported"""
        try:
            from app.main import app
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to import app: {e}")

    def test_project_structure(self):
        """Test basic project structure exists"""
        required_paths = ['app/main.py', 'app/__init__.py']
        for path in required_paths:
            self.assertTrue(os.path.exists(path), f"Missing required file: {path}")

    def test_dependencies(self):
        """Test that core dependencies can be imported"""
        try:
            import fastapi
            import sqlite3
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Missing dependency: {e}")

if __name__ == '__main__':
    unittest.main()
