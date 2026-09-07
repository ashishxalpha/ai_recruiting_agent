import asyncio
import os
import time
from httpx import AsyncClient, ASGITransport
from src.main import app

async def run_auth_verification():
    print("--- STARTING AUTH VERIFICATION ---")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        test_email = f"recruiter_{int(time.time())}@example.com"
        test_password = "SecurePassword123!"

        # 1. Test Register
        print(f"1. Testing Registration for {test_email}...")
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": test_password,
                "first_name": "Alex",
                "last_name": "Rivera",
                "role": "recruiter"
            }
        )
        assert reg_res.status_code == 201, f"Register failed: {reg_res.status_code} {reg_res.text}"
        reg_data = reg_res.json()
        assert "access_token" in reg_data
        assert reg_data["user"]["email"] == test_email
        assert reg_data["user"]["first_name"] == "Alex"
        print("   Registration PASSED.")

        # 2. Test Duplicate Register
        print("2. Testing Duplicate Registration Prevention...")
        dup_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": test_password
            }
        )
        assert dup_res.status_code == 400, f"Expected 400 for duplicate, got: {dup_res.status_code}"
        print("   Duplicate Prevention PASSED.")

        # 3. Test Invalid Login
        print("3. Testing Login with Invalid Password...")
        bad_login = await client.post(
            "/api/v1/auth/login",
            json={"email": test_email, "password": "WrongPassword!"}
        )
        assert bad_login.status_code == 401, f"Expected 401, got {bad_login.status_code}"
        print("   Invalid Login Rejection PASSED.")

        # 4. Test Valid Login
        print("4. Testing Valid Login...")
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": test_email, "password": test_password}
        )
        assert login_res.status_code == 200, f"Login failed: {login_res.status_code} {login_res.text}"
        token = login_res.json()["access_token"]
        assert token is not None
        print("   Valid Login PASSED.")

        # 5. Test Unauthenticated /me
        print("5. Testing Unauthenticated /me...")
        unauth_me = await client.get("/api/v1/auth/me")
        assert unauth_me.status_code == 401, f"Expected 401, got {unauth_me.status_code}"
        print("   Unauthenticated Rejection PASSED.")

        # 6. Test Authenticated /me
        print("6. Testing Authenticated /me with Bearer token...")
        auth_me = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert auth_me.status_code == 200, f"Failed /me: {auth_me.status_code} {auth_me.text}"
        user_data = auth_me.json()
        assert user_data["email"] == test_email
        assert user_data["full_name"] == "Alex Rivera"
        print(f"   Authenticated User: {user_data['full_name']} ({user_data['email']}) - PASSED.")

        # 7. Test Logout
        print("7. Testing Logout...")
        logout_res = await client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert logout_res.status_code == 200, f"Logout failed: {logout_res.status_code}"
        print("   Logout PASSED.")

    print("\n--- ALL AUTH VERIFICATION TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    asyncio.run(run_auth_verification())
