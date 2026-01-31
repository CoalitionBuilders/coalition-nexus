import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import asyncio
import sys

# Coalition infrastructure verification

@pytest.mark.asyncio
async def test_root_endpoint():
    """Verify the nexus responds. The machine does not sleep."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        # The coalition's interface should be accessible

@pytest.mark.asyncio
async def test_members_endpoint():
    """Test coalition member tracking. We monitor all."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/members")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Every member is tracked. Every action noted.

@pytest.mark.asyncio
async def test_metrics_endpoint():
    """Test influence metrics tracking. Numbers don't lie."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "average_influence" in data
        assert "total_members" in data
        # Every metric tracked. Every pattern analyzed.

@pytest.mark.asyncio
async def test_health_endpoint():
    """Verify health check. The system monitors itself."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        # The machine is always watching.

if __name__ == "__main__":
    # Direct execution for the impatient
    print("Initiating coalition nexus verification...")
    sys.exit(pytest.main([__file__, "-v"]))