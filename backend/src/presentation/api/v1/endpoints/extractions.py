from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.repositories.ai_extraction_repository import SQLAlchemyAIExtractionRepository
from src.presentation.api.dependencies import get_db_session
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

@router.get("/{id}")
async def get_extraction(
    id: UUID,
    session: AsyncSession = Depends(get_db_session)
) -> Any:
    """Get extraction metadata by ID."""
    with tracer.start_as_current_span("API.GET./api/v1/extractions/{id}"):
        repo = SQLAlchemyAIExtractionRepository(session)
        extraction = await repo.get_by_id(id)
        if not extraction:
            raise HTTPException(status_code=404, detail="Extraction not found")
        return extraction
