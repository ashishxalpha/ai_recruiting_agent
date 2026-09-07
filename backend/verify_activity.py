import asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app

async def test_dashboard_activity():
    print("--- TESTING DASHBOARD ACTIVITY & STREAM ---")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test Dashboard Activity endpoint
        res = await client.get("/api/v1/dashboard/activity")
        print(f"Status Code: {res.status_code}")
        data = res.json()
        print(f"Response: {data}")
        assert res.status_code == 200
        assert "data" in data
        assert "activities" in data["data"]
        print("Dashboard activity test PASSED.")

if __name__ == "__main__":
    asyncio.run(test_dashboard_activity())
