from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from abc import ABC, abstractmethod

from src.domain.auth.enums import Role

@dataclass
class User:
    id: UUID
    email: str
    role: Role
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
@dataclass
class UserSession:
    id: UUID
    user_id: UUID
    refresh_token_hash: str
    expires_at: datetime
    last_used_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_revoked: bool = False
    created_at: Optional[datetime] = None

@dataclass
class PasswordResetToken:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    is_used: bool = False
    created_at: Optional[datetime] = None

class IdentityProvider(ABC):
    @abstractmethod
    async def authenticate(self, credentials: dict) -> Optional[User]:
        pass

class PasswordIdentityProvider(IdentityProvider):
    pass
