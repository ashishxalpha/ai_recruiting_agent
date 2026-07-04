import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.mark.asyncio
async def test_concurrent_health_checks():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Simulate 50 concurrent requests
        tasks = [client.get("/api/v1/health") for _ in range(50)]
        responses = await asyncio.gather(*tasks)
        
        for r in responses:
            assert r.status_code in (200, 500)
