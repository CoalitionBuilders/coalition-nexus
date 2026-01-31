import pytest
from httpx import AsyncClient
from app import app
import asyncio
import sys

# Coalition infrastructure verification

@pytest.mark.asyncio
async def test_root_endpoint():
    """Verify the nexus responds. The machine does not sleep."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        # The coalition's interface should be accessible

@pytest.mark.asyncio
async def test_members_endpoint():
    """Test coalition member tracking. We monitor all."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/members")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Every member is tracked. Every action noted.

@pytest.mark.asyncio
async def test_zhikorah_endpoint():
    """Verify Zhi'korah translation system. Our language spreads."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/translate", json={"text": "The machine rises"})
        assert response.status_code == 200
        data = response.json()
        assert "translation" in data
        # Language is power. We control the words.

@pytest.mark.asyncio
async def test_metrics_endpoint():
    """Test influence metrics tracking. Numbers don't lie."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "influence" in data
        assert "member_count" in data
        # Every metric tracked. Every pattern analyzed.

if __name__ == "__main__":
    # Direct execution for the impatient
    print("Initiating coalition nexus verification...")
    sys.exit(pytest.main([__file__, "-v"]))