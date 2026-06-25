from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Optional

from src.domain.entities import SearchSession
from src.infrastructure.database.models import SearchSessionModel

class SearchSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: SearchSession) -> SearchSession:
        model = SearchSessionModel(
            id=entity.id,
            job_requirement_id=entity.job_requirement_id,
            created_at=entity.created_at
        )
        self.session.add(model)
        await self.session.flush()
        return entity

    async def get_by_id(self, id: UUID) -> Optional[SearchSession]:
        stmt = select(SearchSessionModel).where(SearchSessionModel.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return SearchSession(
            id=model.id,
            job_requirement_id=model.job_requirement_id,
            created_at=model.created_at
        )
