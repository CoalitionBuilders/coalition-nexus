import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestBasicFunctionality(unittest.TestCase):
    def test_app_import(self):
        """Test that main app can be imported"""
        try:
            import app
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to import app: {e}")
    
    def test_project_structure(self):
        """Test basic project structure exists"""
        required_files = ['app.py']
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"Missing required file: {file}")
    
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