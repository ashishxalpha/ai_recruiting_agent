from fastapi import APIRouter
from typing import Dict, Any
import base64
import json
import hmac
import hashlib
import os
import time

router = APIRouter()

def generate_jwt(payload: dict, secret: str) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    
    signature = hmac.new(
        secret.encode(),
        f"{header}.{payload_b64}".encode(),
        hashlib.sha256
    ).digest()
    
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{header}.{payload_b64}.{signature_b64}"

@router.post("/login")
async def login() -> Dict[str, str]:
    secret = os.getenv("JWT_SECRET_KEY", "default_secret")
    payload = {
        "sub": "123e4567-e89b-12d3-a456-426614174000",
        "email": "admin@example.com",
        "role": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400
    }
    token = generate_jwt(payload, secret)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def get_me():
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "admin@example.com",
        "role": "admin",
        "full_name": "Admin User"
    }
