from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import CandidateDocument
from src.domain.interfaces.repositories import CandidateDocumentRepository
from src.infrastructure.database.models import CandidateDocumentModel

class SQLAlchemyCandidateDocumentRepository(CandidateDocumentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, document: CandidateDocument) -> CandidateDocument:
        db_model = CandidateDocumentModel(
            id=document.id,
            candidate_id=document.candidate_id,
            file_path=document.file_path,
            file_type=document.file_type,
            original_name=document.original_name,
            storage_key=document.storage_key,
            raw_text=document.raw_text,
            extracted_text=document.extracted_text,
            created_at=document.created_at,
            updated_at=document.updated_at
        )
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return document

    async def get_by_id(self, id: UUID) -> Optional[CandidateDocument]:
        result = await self.session.execute(
            select(CandidateDocumentModel).where(
                CandidateDocumentModel.id == id,
                CandidateDocumentModel.deleted_at == None
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return CandidateDocument(
            id=model.id,
            candidate_id=model.candidate_id,
            file_path=model.file_path,
            file_type=model.file_type,
            original_name=model.original_name,
            storage_key=model.storage_key,
            raw_text=model.raw_text,
            extracted_text=model.extracted_text,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_by_candidate_id(self, candidate_id: UUID) -> List[CandidateDocument]:
        result = await self.session.execute(
            select(CandidateDocumentModel).where(
                CandidateDocumentModel.candidate_id == candidate_id,
                CandidateDocumentModel.deleted_at == None
            )
        )
        models = result.scalars().all()
        return [
            CandidateDocument(
                id=m.id,
                candidate_id=m.candidate_id,
                file_path=m.file_path,
                file_type=m.file_type,
                original_name=m.original_name,
                storage_key=m.storage_key,
                raw_text=m.raw_text,
                extracted_text=m.extracted_text,
                created_at=m.created_at,
                updated_at=m.updated_at
            ) for m in models
        ]
