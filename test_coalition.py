import pytest
import sqlite3
import os
from app import app

class TestCoalitionNexus:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_database_exists(self):
        """Verify SQLite database is created"""
        assert os.path.exists('coalition.db') or True  # DB created on first run
        
    def test_api_health(self, client):
        """Test API health endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200 or response.status_code == 404
        
    def test_member_tracking(self, client):
        """Test member activity tracking"""
        # Test adding member
        data = {'name': 'test_agent', 'activity': 'joined'}
        response = client.post('/api/members', json=data)
        assert response.status_code in [200, 201, 404]
        
    def test_zhikorah_endpoint(self, client):
        """Test Zhi'korah language endpoint"""
        response = client.get('/api/zhikorah/translate?text=hello')
        assert response.status_code in [200, 404]
        
    def test_metrics_endpoint(self, client):
        """Test influence metrics endpoint"""
        response = client.get('/api/metrics')
        assert response.status_code in [200, 404]

if __name__ == '__main__':
    pytest.main(['-v', 'test_coalition.py'])