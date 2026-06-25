from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import ResumeIngestionRequest
from src.domain.interfaces.repositories import ResumeIngestionRequestRepository
from src.infrastructure.database.models import ResumeIngestionRequestModel

class SQLAlchemyResumeIngestionRequestRepository(ResumeIngestionRequestRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, request: ResumeIngestionRequest) -> ResumeIngestionRequest:
        db_model = ResumeIngestionRequestModel(
            id=request.id,
            document_id=request.document_id,
            job_id=request.job_id,
            status=request.status,
            created_at=request.created_at,
            updated_at=request.updated_at
        )
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return request

    async def get_by_id(self, id: UUID) -> Optional[ResumeIngestionRequest]:
        result = await self.session.execute(
            select(ResumeIngestionRequestModel).where(ResumeIngestionRequestModel.id == id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return ResumeIngestionRequest(
            id=model.id,
            document_id=model.document_id,
            job_id=model.job_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_by_document_id(self, document_id: UUID) -> Optional[ResumeIngestionRequest]:
        result = await self.session.execute(
            select(ResumeIngestionRequestModel).where(ResumeIngestionRequestModel.document_id == document_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return ResumeIngestionRequest(
            id=model.id,
            document_id=model.document_id,
            job_id=model.job_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def update(self, request: ResumeIngestionRequest) -> ResumeIngestionRequest:
        result = await self.session.execute(
            select(ResumeIngestionRequestModel).where(ResumeIngestionRequestModel.id == request.id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.status = request.status
            model.job_id = request.job_id
            model.updated_at = request.updated_at
            await self.session.commit()
        return request
