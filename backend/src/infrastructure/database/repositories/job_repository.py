from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import BackgroundJob
from src.domain.interfaces.repositories import JobRepository
from src.infrastructure.database.models import BackgroundJobModel

class SQLAlchemyJobRepository(JobRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, job: BackgroundJob) -> BackgroundJob:
        db_model = BackgroundJobModel(
            id=job.id,
            job_type=job.job_type,
            correlation_id=job.correlation_id,
            status=job.status,
            payload=job.payload,
            result=job.result,
            error_message=job.error_message,
            started_at=job.started_at,
            completed_at=job.completed_at,
            created_at=job.created_at,
            updated_at=job.updated_at
        )
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return job

    async def get_by_id(self, id: UUID) -> Optional[BackgroundJob]:
        result = await self.session.execute(
            select(BackgroundJobModel).where(BackgroundJobModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return BackgroundJob(
            id=model.id,
            job_type=model.job_type,
            correlation_id=model.correlation_id,
            status=model.status,
            payload=model.payload,
            result=model.result,
            error_message=model.error_message,
            started_at=model.started_at,
            completed_at=model.completed_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def update(self, job: BackgroundJob) -> BackgroundJob:
        result = await self.session.execute(
            select(BackgroundJobModel).where(BackgroundJobModel.id == job.id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.status = job.status
            model.result = job.result
            model.error_message = job.error_message
            model.started_at = job.started_at
            model.completed_at = job.completed_at
            model.updated_at = job.updated_at
            await self.session.commit()
        return job
