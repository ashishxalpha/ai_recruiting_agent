from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import AIExtraction
from src.domain.interfaces.repositories import AIExtractionRepository
from src.infrastructure.database.models import AIExtractionModel

class SQLAlchemyAIExtractionRepository(AIExtractionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, extraction: AIExtraction) -> AIExtraction:
        db_model = AIExtractionModel(
            id=extraction.id,
            document_id=extraction.document_id,
            provider=extraction.provider,
            model_name=extraction.model_name,
            prompt_version=extraction.prompt_version,
            schema_version=extraction.schema_version,
            raw_ai_response=extraction.raw_ai_response,
            normalized_response=extraction.normalized_response,
            confidence_score=extraction.confidence_score,
            created_at=extraction.created_at,
            updated_at=extraction.updated_at
        )
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return extraction

    async def get_by_document_id(self, document_id: UUID) -> List[AIExtraction]:
        result = await self.session.execute(
            select(AIExtractionModel).where(
                AIExtractionModel.document_id == document_id,
                AIExtractionModel.deleted_at == None
            ).order_by(AIExtractionModel.created_at.desc())
        )
        models = result.scalars().all()
        return [
            AIExtraction(
                id=m.id,
                document_id=m.document_id,
                provider=m.provider,
                model_name=m.model_name,
                prompt_version=m.prompt_version,
                schema_version=m.schema_version,
                raw_ai_response=m.raw_ai_response,
                normalized_response=m.normalized_response,
                confidence_score=m.confidence_score,
                created_at=m.created_at,
                updated_at=m.updated_at,
                deleted_at=m.deleted_at
            ) for m in models
        ]
