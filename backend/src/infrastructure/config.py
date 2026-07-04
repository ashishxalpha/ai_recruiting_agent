import os

def get_db_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Fallback to dev SQLite if in dev, but in prod we should fail fast
        if os.getenv("ENVIRONMENT") == "production":
            raise ValueError("DATABASE_URL must be set in production")
        return "sqlite+aiosqlite:///test.db"
    return db_url

def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        if os.getenv("ENVIRONMENT") == "production":
            raise ValueError("OPENAI_API_KEY must be set in production")
        return "dummy_key"
    return api_key

def get_environment() -> str:
    return os.getenv("ENVIRONMENT", "development")

def get_jwt_secret_key() -> str:
    key = os.getenv("JWT_SECRET_KEY")
    if not key:
        if get_environment() == "production":
            raise ValueError("JWT_SECRET_KEY must be set in production")
        return "super-secret-development-key"
    return key

def get_jwt_algorithm() -> str:
    return os.getenv("JWT_ALGORITHM", "HS256")

def get_access_token_expire_minutes() -> int:
    return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

def get_refresh_token_expire_days() -> int:
    return int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
