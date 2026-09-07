from typing import Tuple
from fastapi import HTTPException, status
from src.infrastructure.database.models import UserModel
from src.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.infrastructure.auth.security import hash_password, verify_password, create_access_token
from src.application.schemas.auth import UserRegisterRequest, UserLoginRequest

class AuthService:
    def __init__(self, user_repo: SQLAlchemyUserRepository):
        self.user_repo = user_repo

    async def register(self, request: UserRegisterRequest) -> Tuple[UserModel, str]:
        normalized_email = request.email.lower().strip()
        existing = await self.user_repo.get_by_email(normalized_email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )

        hashed_pw = hash_password(request.password)
        user = UserModel(
            email=normalized_email,
            hashed_password=hashed_pw,
            first_name=request.first_name,
            last_name=request.last_name,
            role=request.role or "recruiter",
            is_active=True
        )
        created_user = await self.user_repo.create(user)

        token = create_access_token({
            "sub": str(created_user.id),
            "email": created_user.email,
            "role": created_user.role
        })
        return created_user, token

    async def authenticate(self, request: UserLoginRequest) -> Tuple[UserModel, str]:
        normalized_email = request.email.lower().strip()
        user = await self.user_repo.get_by_email(normalized_email)
        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user account."
            )

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        })
        return user, token
