import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from src.infrastructure.config import (
    get_jwt_secret_key,
    get_jwt_algorithm,
    get_access_token_expire_minutes,
    get_refresh_token_expire_days
)

class JWTProvider:
    def __init__(self):
        self.secret_key = get_jwt_secret_key()
        self.algorithm = get_jwt_algorithm()
        self.access_token_expire_minutes = get_access_token_expire_minutes()
        self.refresh_token_expire_days = get_refresh_token_expire_days()

    def create_access_token(self, subject: str, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {"sub": subject, "role": role, "exp": expire, "token_type": "access"}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, subject: str, session_id: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        to_encode = {"sub": subject, "session_id": session_id, "exp": expire, "token_type": "refresh"}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
