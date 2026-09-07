from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from src.application.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse
)
from src.application.services.auth_service import AuthService
from src.presentation.api.dependencies import get_auth_service, get_current_user
from src.infrastructure.database.models import UserModel

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: UserRegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> Dict[str, Any]:
    user, token = await auth_service.register(request)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.from_user(user).model_dump(mode="json")
    }

@router.post("/login")
async def login(
    request: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> Dict[str, Any]:
    user, token = await auth_service.authenticate(request)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.from_user(user).model_dump(mode="json")
    }

@router.get("/me")
async def get_me(
    current_user: UserModel = Depends(get_current_user)
) -> Dict[str, Any]:
    return UserResponse.from_user(current_user).model_dump(mode="json")

@router.post("/logout")
async def logout(
    current_user: UserModel = Depends(get_current_user)
) -> Dict[str, str]:
    return {"message": "Logged out successfully"}
