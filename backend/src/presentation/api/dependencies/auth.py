from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from src.infrastructure.database.base import async_session_maker
from src.infrastructure.auth.user_repository import UserRepository
from src.application.auth.token_service import TokenService
from src.infrastructure.auth.jwt_provider import JWTProvider
from src.infrastructure.database.models import UserModel
from src.domain.auth.enums import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

def get_token(request: Request, token: Optional[str] = Depends(oauth2_scheme)) -> Optional[str]:
    # Extract token from cookie first, fallback to Authorization header
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        # Check if the cookie value is "Bearer <token>" or just "<token>"
        if cookie_token.startswith("Bearer "):
            return cookie_token.split(" ")[1]
        return cookie_token
    return token

async def get_current_user(token: Optional[str] = Depends(get_token)) -> UserModel:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    jwt_provider = JWTProvider()
    token_service = TokenService(jwt_provider)
    payload = token_service.decode(token)
    
    if not payload or payload.get("token_type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
        
    async with async_session_maker() as db:
        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(UUID(user_id_str))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
            
        return user

def require_role(allowed_roles: list[Role]):
    async def role_checker(current_user: UserModel = Depends(get_current_user)) -> UserModel:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return current_user
    return role_checker
