from typing import Optional, Dict, Any
from src.infrastructure.auth.jwt_provider import JWTProvider

class TokenService:
    def __init__(self, jwt_provider: JWTProvider):
        self.provider = jwt_provider

    def create_access_token(self, subject: str, role: str) -> str:
        return self.provider.create_access_token(subject, role)

    def create_refresh_token(self, subject: str, session_id: str) -> str:
        return self.provider.create_refresh_token(subject, session_id)

    def decode(self, token: str) -> Optional[Dict[str, Any]]:
        return self.provider.decode_token(token)
