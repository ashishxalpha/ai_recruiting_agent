from src.infrastructure.auth.bcrypt_provider import BcryptProvider

class PasswordService:
    def __init__(self, bcrypt_provider: BcryptProvider):
        self.provider = bcrypt_provider

    def hash(self, password: str) -> str:
        # In a real app, we could validate complexity here (e.g., len >= 8, etc.)
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return self.provider.get_password_hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.provider.verify_password(plain_password, hashed_password)
