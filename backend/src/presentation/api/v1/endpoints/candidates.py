from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from typing import Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.api.dependencies import get_db_session
from src.application.services.candidate_query_service import CandidateQueryService
from src.application.schemas.candidate import CandidateSummaryDTO, CandidateDetailsDTO
from src.application.schemas.pagination import PaginatedResponse
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

def get_candidate_query_service(db: AsyncSession = Depends(get_db_session)) -> CandidateQueryService:
    return CandidateQueryService(db)

@router.get("", response_model=PaginatedResponse[CandidateSummaryDTO])
async def list_candidates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    service: CandidateQueryService = Depends(get_candidate_query_service)
) -> PaginatedResponse[CandidateSummaryDTO]:
    with tracer.start_as_current_span("API.GET./api/v1/candidates"):
        return await service.list_candidates(
            page=page, 
            page_size=page_size, 
            search=search, 
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )

@router.get("/{id}", response_model=CandidateDetailsDTO)
async def get_candidate(
    id: UUID,
    service: CandidateQueryService = Depends(get_candidate_query_service)
) -> CandidateDetailsDTO:
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}"):
        candidate = await service.get_candidate_details(id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return candidate

@router.get("/{id}/workflow")
async def get_candidate_workflow(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/evaluation")
async def get_candidate_evaluation(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/embeddings")
async def get_candidate_embeddings(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/memory")
async def get_candidate_memory(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/matches")
async def get_candidate_matches(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/feedback")
async def get_candidate_feedback(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/documents")
async def get_candidate_documents(
    id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}/documents"):
        # Temporary direct DB fetch until DocumentQueryService is added
        from sqlalchemy import select
        from src.infrastructure.database.models import CandidateDocumentModel
        stmt = select(CandidateDocumentModel).where(CandidateDocumentModel.candidate_id == id)
        result = await db.execute(stmt)
        docs = result.scalars().all()
        return [{"id": d.id, "original_name": d.original_name, "file_type": d.file_type} for d in docs]
