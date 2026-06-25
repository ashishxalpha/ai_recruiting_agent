from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from typing import Any, List

from src.application.services.candidate_service import CandidateService
from src.presentation.api.dependencies import get_candidate_service
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

@router.get("")
async def list_candidates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: CandidateService = Depends(get_candidate_service)
) -> List[Any]:
    with tracer.start_as_current_span("API.GET./api/v1/candidates"):
        return await service.list_candidates(skip=skip, limit=limit)

@router.get("/{id}")
async def get_candidate(
    id: UUID,
    service: CandidateService = Depends(get_candidate_service)
) -> Any:
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}"):
        candidate = await service.get_candidate(id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return candidate

@router.get("/{id}/documents")
async def get_candidate_documents(
    id: UUID,
    service: CandidateService = Depends(get_candidate_service)
) -> List[Any]:
    with tracer.start_as_current_span("API.GET./api/v1/candidates/{id}/documents"):
        return await service.get_documents(id)
