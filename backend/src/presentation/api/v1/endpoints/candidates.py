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
async def get_candidate_workflow(id: UUID, db: AsyncSession = Depends(get_db_session)):
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}/workflow"):
        from sqlalchemy import select
        from src.infrastructure.database.models import WorkflowExecutionModel
        stmt = select(WorkflowExecutionModel).where(WorkflowExecutionModel.candidate_id == id)
        result = await db.execute(stmt)
        executions = result.scalars().all()
        return [{
            "id": e.id, 
            "workflow_name": e.workflow_name, 
            "status": e.status, 
            "current_node": e.current_node,
            "started_at": e.started_at,
            "completed_at": e.completed_at
        } for e in executions]

@router.get("/{id}/evaluation")
async def get_candidate_evaluation(id: UUID, db: AsyncSession = Depends(get_db_session)):
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}/evaluation"):
        from sqlalchemy import select
        from src.infrastructure.database.models import CandidateMatchModel
        stmt = select(CandidateMatchModel).where(CandidateMatchModel.candidate_id == id)
        result = await db.execute(stmt)
        matches = result.scalars().all()
        return [{"id": m.id, "job_requirement_id": m.search_session_id, "final_score": m.final_score} for m in matches]

@router.get("/{id}/embeddings")
async def get_candidate_embeddings(id: UUID, db: AsyncSession = Depends(get_db_session)):
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}/embeddings"):
        from sqlalchemy import select
        from src.infrastructure.database.models import CandidateEmbeddingModel
        stmt = select(CandidateEmbeddingModel).where(CandidateEmbeddingModel.candidate_id == id)
        result = await db.execute(stmt)
        embeddings = result.scalars().all()
        return [{
            "id": e.id, 
            "embedding_type": e.embedding_type, 
            "embedding_model": e.embedding_model,
            "vector_preview": e.vector_data[:5] if e.vector_data else [],
            "dimensions": len(e.vector_data) if e.vector_data else 0
        } for e in embeddings]

@router.get("/{id}/memory")
async def get_candidate_memory(id: UUID):
    # For now, memory isn't directly linked to candidates in the same way, return empty list
    return []

@router.get("/{id}/matches")
async def get_candidate_matches(id: UUID, db: AsyncSession = Depends(get_db_session)):
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}/matches"):
        from sqlalchemy import select
        from src.infrastructure.database.models import CandidateMatchModel
        stmt = select(CandidateMatchModel).where(CandidateMatchModel.candidate_id == id)
        result = await db.execute(stmt)
        matches = result.scalars().all()
        return [{"id": m.id, "job_requirement_id": m.search_session_id, "semantic_score": m.semantic_score} for m in matches]

@router.get("/{id}/feedback")
async def get_candidate_feedback(id: UUID, db: AsyncSession = Depends(get_db_session)):
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}/feedback"):
        from sqlalchemy import select
        from src.infrastructure.database.models import CandidateMatchModel, RecruiterFeedbackModel
        # Join feedback through match
        stmt = select(RecruiterFeedbackModel).join(CandidateMatchModel).where(CandidateMatchModel.candidate_id == id)
        result = await db.execute(stmt)
        feedbacks = result.scalars().all()
        return [{"id": f.id, "decision": f.decision, "confidence": f.confidence, "created_at": f.created_at} for f in feedbacks]

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
