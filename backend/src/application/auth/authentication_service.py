from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
from fastapi import HTTPException, status

from src.infrastructure.auth.user_repository import UserRepository
from src.infrastructure.auth.session_repository import SessionRepository
from src.application.auth.password_service import PasswordService
from src.application.auth.token_service import TokenService
from src.infrastructure.database.models import UserModel
from src.application.schemas.auth import UserRegisterDTO, UserLoginDTO
from src.domain.auth.enums import Role
from src.infrastructure.config import get_refresh_token_expire_days

class AuthenticationService:
    def __init__(
        self,
        user_repo: UserRepository,
        session_repo: SessionRepository,
        password_service: PasswordService,
        token_service: TokenService
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.password_service = password_service
        self.token_service = token_service

    async def register(self, dto: UserRegisterDTO) -> UserModel:
        existing_user = await self.user_repo.get_by_email(dto.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        hashed_password = self.password_service.hash(dto.password)
        new_user = UserModel(
            email=dto.email,
            hashed_password=hashed_password,
            first_name=dto.first_name,
            last_name=dto.last_name,
            role=Role.VIEWER
        )
        return await self.user_repo.create(new_user)

    async def login(self, dto: UserLoginDTO, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Tuple[str, str]:
        # returns (access_token, refresh_token)
        user = await self.user_repo.get_by_email(dto.email)
        if not user or not self.password_service.verify(dto.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

        access_token = self.token_service.create_access_token(subject=str(user.id), role=user.role.value)
        
        # Create a session
        expire_days = get_refresh_token_expire_days()
        expires_at = datetime.now(timezone.utc) + timedelta(days=expire_days)
        # Generate dummy refresh token for hash (in a real app, generate a secure random string)
        import secrets
        raw_refresh_token = secrets.token_urlsafe(32)
        refresh_token_hash = self.password_service.hash(raw_refresh_token)
        
        session = await self.session_repo.create_session(
            user_id=user.id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        refresh_token = self.token_service.create_refresh_token(subject=str(user.id), session_id=str(session.id))
        return access_token, refresh_token

    async def logout(self, session_id: UUID) -> None:
        await self.session_repo.revoke_session(session_id)
        
    async def refresh(self, refresh_token: str) -> Tuple[str, str]:
        # Decodes the token, checks the session, rotates the tokens
        payload = self.token_service.decode(refresh_token)
        if not payload or payload.get("token_type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
            
        session_id_str = payload.get("session_id")
        user_id_str = payload.get("sub")
        if not session_id_str or not user_id_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
            
        session_id = UUID(session_id_str)
        session = await self.session_repo.get_session(session_id)
        
        if not session or session.is_revoked or session.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or revoked")
            
        # Revoke old session
        await self.session_repo.revoke_session(session_id)
        
        user = await self.user_repo.get_by_id(UUID(user_id_str))
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User disabled or not found")
            
        access_token = self.token_service.create_access_token(subject=str(user.id), role=user.role.value)
        
        expire_days = get_refresh_token_expire_days()
        expires_at = datetime.now(timezone.utc) + timedelta(days=expire_days)
        
        import secrets
        raw_refresh_token = secrets.token_urlsafe(32)
        refresh_token_hash = self.password_service.hash(raw_refresh_token)
        
        new_session = await self.session_repo.create_session(
            user_id=user.id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            ip_address=session.ip_address,
            user_agent=session.user_agent
        )
        
        new_refresh_token = self.token_service.create_refresh_token(subject=str(user.id), session_id=str(new_session.id))
        return access_token, new_refresh_token
