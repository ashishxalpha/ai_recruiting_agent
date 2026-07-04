from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.infrastructure.database.models import UserSessionModel

class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, user_id: UUID, refresh_token_hash: str, expires_at: datetime, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> UserSessionModel:
        db_session = UserSessionModel(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            last_used_at=datetime.now(timezone.utc),
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.add(db_session)
        await self.db.commit()
        await self.db.refresh(db_session)
        return db_session

    async def get_session(self, session_id: UUID) -> Optional[UserSessionModel]:
        stmt = select(UserSessionModel).where(UserSessionModel.id == session_id, UserSessionModel.is_revoked == False)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update_last_used(self, session_id: UUID) -> None:
        stmt = update(UserSessionModel).where(UserSessionModel.id == session_id).values(last_used_at=datetime.now(timezone.utc))
        await self.db.execute(stmt)
        await self.db.commit()

    async def revoke_session(self, session_id: UUID) -> None:
        stmt = update(UserSessionModel).where(UserSessionModel.id == session_id).values(is_revoked=True)
        await self.db.execute(stmt)
        await self.db.commit()
