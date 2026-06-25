from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Optional, List

from src.domain.entities import JobRequirement
from src.infrastructure.database.models import JobRequirementModel

class JobRequirementRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: JobRequirementModel) -> JobRequirement:
        return JobRequirement(
            id=model.id,
            title=model.title,
            description=model.description,
            skills_required=model.skills_required,
            experience_required=model.experience_required,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: JobRequirement) -> JobRequirementModel:
        return JobRequirementModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            skills_required=entity.skills_required,
            experience_required=entity.experience_required,
            status=entity.status
        )

    async def create(self, requirement: JobRequirement) -> JobRequirement:
        model = self._to_model(requirement)
        self.session.add(model)
        await self.session.flush()
        return self._to_entity(model)

    async def get_by_id(self, id: UUID) -> Optional[JobRequirement]:
        stmt = select(JobRequirementModel).where(JobRequirementModel.id == id, JobRequirementModel.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_entity(model)
