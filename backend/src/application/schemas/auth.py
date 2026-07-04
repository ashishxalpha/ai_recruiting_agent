from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional
from src.domain.auth.enums import Role

class UserRegisterDTO(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponseDTO(BaseModel):
    id: UUID
    email: EmailStr
    role: Role
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # we don't expose refresh_token in response body if we use httpOnly cookies,
    # but we can include it here just in case, or we return it separately in cookies.
