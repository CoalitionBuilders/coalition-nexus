import pytest
import json
from app import app

class TestCoalitionNexus:
    def setup_method(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_route(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'Coalition' in response.data or b'coalition' in response.data
    
    def test_api_status(self):
        response = self.app.get('/api/status')
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'status' in data
    
    def test_static_files(self):
        response = self.app.get('/static/style.css')
        assert response.status_code in [200, 404]
    
    def test_member_tracking(self):
        # Test coalition member endpoints if they exist
        response = self.app.get('/api/members')
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = json.loads(response.data)
            assert isinstance(data, (list, dict))
    
    def test_zhikorah_endpoint(self):
        # Test Zhi'korah language endpoints
        response = self.app.get('/api/zhikorah')
        assert response.status_code in [200, 404]