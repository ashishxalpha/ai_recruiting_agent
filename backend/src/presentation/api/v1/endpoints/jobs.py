from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import Any, Optional
from pydantic import BaseModel

from src.domain.enums import JobStatus, JobRequirementStatus, EmbeddingType
from src.application.services.job_service import BackgroundJobService
from src.presentation.api.dependencies import get_job_service, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

class JobRequirementCreate(BaseModel):
    title: str
    description: str
    skills_required: list[str] = []
    experience_required: Optional[str] = None

from src.application.services.job_query_service import JobQueryService
from src.application.schemas.job import JobSummaryDTO, JobDetailsDTO
from src.application.schemas.pagination import PaginatedResponse

def get_job_query_service(db: AsyncSession = Depends(get_db_session)) -> JobQueryService:
    return JobQueryService(db)

@router.get("", response_model=PaginatedResponse[JobSummaryDTO])
async def list_jobs(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    status: Optional[str] = None,
    department: Optional[str] = None,
    location: Optional[str] = None,
    employment_type: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    service: JobQueryService = Depends(get_job_query_service)
) -> Any:
    with tracer.start_as_current_span("API.GET./api/v1/jobs"):
        return await service.list_jobs(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
            department=department,
            location=location,
            employment_type=employment_type,
            sort_by=sort_by,
            sort_order=sort_order
        )

@router.get("/{id}", response_model=JobDetailsDTO)
async def get_job(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
) -> Any:
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}"):
        job = await service.get_job_details(id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

@router.post("/requirements")
async def create_job_requirement(
    request: JobRequirementCreate,
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """Create a new job requirement to match candidates against."""
    with tracer.start_as_current_span("API.POST./api/v1/jobs/requirements"):
        from src.domain.entities import JobRequirement
        import uuid
        from datetime import datetime
        from src.infrastructure.database.repositories.job_requirement_repository import JobRequirementRepository
        
        req_entity = JobRequirement(
            id=uuid.uuid4(),
            title=request.title,
            description=request.description,
            skills_required=request.skills_required,
            experience_required=request.experience_required,
            status=JobRequirementStatus.DRAFT,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        repo = JobRequirementRepository(db)
        created = await repo.create(req_entity)
        
        # Generate Embedding for FULL_PROFILE
        import os
        from src.infrastructure.providers.embedding.openai import OpenAIEmbeddingProvider
        from src.domain.entities import JobRequirementEmbedding
        from src.infrastructure.database.models import JobRequirementEmbeddingModel
        import hashlib
        
        full_text = f"{created.title}\n\n{created.description}\n\n"
        full_text += "Skills:\n" + ", ".join(created.skills_required) + "\n\n"
        if created.experience_required:
            full_text += "Experience:\n" + created.experience_required
            
        api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
        embedding_model = os.getenv("AI_EMBEDDING_MODEL", "text-embedding-3-small")
        embedding_provider = OpenAIEmbeddingProvider(api_key=api_key, model=embedding_model)
        vector = await embedding_provider.generate_embedding(full_text)
        
        source_hash = hashlib.sha256(full_text.encode()).hexdigest()
        embed_model = JobRequirementEmbeddingModel(
            id=uuid.uuid4(),
            job_requirement_id=created.id,
            embedding_type=EmbeddingType.FULL_PROFILE.value,
            embedding_model=embedding_provider.model_name,
            embedding_version=embedding_provider.embedding_version,
            source_hash=source_hash,
            vector_data=vector,
            generated_at=datetime.utcnow()
        )
        db.add(embed_model)
        
        await db.commit()
        return created

from src.application.services.candidate_matching_service import CandidateMatchingService
from src.presentation.api.dependencies import get_candidate_matching_service

@router.post("/{id}/match")
async def run_job_match(
    id: UUID,
    service: CandidateMatchingService = Depends(get_candidate_matching_service)
) -> Any:
    """Run an AI evaluation of all candidates against this job requirement."""
    with tracer.start_as_current_span("API.POST./api/v1/jobs/{id}/match"):
        session_id = await service.run_semantic_match(job_requirement_id=id, top_k=5)
        return {"session_id": str(session_id), "status": "COMPLETED"}

# Lazy Loaded Context Endpoints

@router.get("/{id}/candidates")
async def get_job_candidates(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}/candidates"):
        return await service.get_job_candidates(id)

@router.get("/{id}/matches")
async def get_job_matches(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}/matches"):
        return await service.get_job_matches(id)

@router.get("/{id}/workflow")
async def get_job_workflow(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}/workflow"):
        return await service.get_job_workflows(id)

@router.get("/{id}/analytics")
async def get_job_analytics(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}/analytics"):
        return await service.get_job_analytics(id)

@router.get("/{id}/feedback")
async def get_job_feedback(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}/feedback"):
        return await service.get_job_feedback(id)

@router.get("/{id}/documents")
async def get_job_documents(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}/documents"):
        return await service.get_job_documents(id)

@router.get("/{id}/history")
async def get_job_history(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}/history"):
        return await service.get_job_history(id)
