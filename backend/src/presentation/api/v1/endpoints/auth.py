from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from src.infrastructure.database.base import get_db
from src.infrastructure.auth.user_repository import UserRepository
from src.infrastructure.auth.session_repository import SessionRepository
from src.application.auth.password_service import PasswordService
from src.application.auth.token_service import TokenService
from src.infrastructure.auth.jwt_provider import JWTProvider
from src.infrastructure.auth.bcrypt_provider import BcryptProvider
from src.application.auth.authentication_service import AuthenticationService

from src.application.schemas.auth import UserRegisterDTO, UserLoginDTO, UserResponseDTO
from src.presentation.api.dependencies.auth import get_current_user
from src.infrastructure.database.models import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthenticationService:
    user_repo = UserRepository(db)
    session_repo = SessionRepository(db)
    pwd_service = PasswordService(BcryptProvider())
    token_service = TokenService(JWTProvider())
    return AuthenticationService(user_repo, session_repo, pwd_service, token_service)

@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(
    dto: UserRegisterDTO,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> Any:
    user = await auth_service.register(dto)
    return user

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    dto: UserLoginDTO,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> Any:
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    access_token, refresh_token = await auth_service.login(dto, ip_address, user_agent)
    
    # Set HttpOnly Cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600 # 1 hour
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7*24*3600 # 7 days
    )
    
    return {"message": "Login successful"}

@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> Any:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
        
    new_access_token, new_refresh_token = await auth_service.refresh(refresh_token)
    
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600
    )
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7*24*3600
    )
    
    return {"message": "Token refreshed"}

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> Any:
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        try:
            # We need to decode to get session ID, auth_service can handle it or we decode here
            token_service = TokenService(JWTProvider())
            payload = token_service.decode(refresh_token)
            if payload and "session_id" in payload:
                from uuid import UUID
                await auth_service.logout(UUID(payload["session_id"]))
        except Exception:
            pass # Ignore errors during logout
            
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponseDTO)
async def get_me(current_user: UserModel = Depends(get_current_user)) -> Any:
    return current_user
