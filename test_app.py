import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

class TestCoalitionNexus:
    @pytest.mark.asyncio
    async def test_home_route(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get('/')
            assert response.status_code == 200
            data = response.json()
            assert 'Coalition' in data.get('message', '') or 'coalition' in str(data).lower()

    @pytest.mark.asyncio
    async def test_api_status(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get('/')
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data

    @pytest.mark.asyncio
    async def test_member_tracking(self):
        # Test coalition member endpoints
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get('/api/members')
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
