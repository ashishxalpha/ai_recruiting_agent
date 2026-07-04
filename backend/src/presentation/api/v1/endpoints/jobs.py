from fastapi import APIRouter
from src.presentation.api.dependencies.auth import get_current_user
from src.infrastructure.database.models import UserModel
, Depends, HTTPException, Query
from uuid import UUID
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.presentation.api.dependencies import get_db_session, get_job_service
from src.application.services.job_service import BackgroundJobService
from src.application.services.jobs.job_query_service import JobQueryService
from src.application.schemas.job import JobSummaryDTO, JobDetailsDTO
from src.application.schemas.pagination import PaginatedResponse
from src.observability.tracing import get_tracer
from src.domain.enums import JobStatus

router = APIRouter()
tracer = get_tracer(__name__)

def get_job_query_service(db: AsyncSession = Depends(get_db_session)) -> JobQueryService:
    return JobQueryService(db)

@router.get("", response_model=PaginatedResponse[JobSummaryDTO])
async def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    department: Optional[str] = None,
    location: Optional[str] = None,
    employment_type: Optional[str] = None,
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    service: JobQueryService = Depends(get_job_query_service)
) -> PaginatedResponse[JobSummaryDTO]:
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
async def get_job_details(
    id: UUID,
    service: JobQueryService = Depends(get_job_query_service)
) -> JobDetailsDTO:
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}"):
        job = await service.get_job_details(id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

# Bounded Context Endpoints (Lazy Loaded Tabs)

@router.get("/{id}/candidates")
async def get_job_candidates(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/matches")
async def get_job_matches(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/workflow")
async def get_job_workflow(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/analytics")
async def get_job_analytics(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/feedback")
async def get_job_feedback(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/documents")
async def get_job_documents(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.get("/{id}/history")
async def get_job_history(id: UUID):
    # To be implemented
    raise HTTPException(status_code=501, detail="feature_available: false")

class JobUpdateRequest(BaseModel):
    status: JobStatus
    error_message: Optional[str] = None

@router.patch("/{id}")
async def update_job(
    id: UUID,
    request: JobUpdateRequest,
    service: BackgroundJobService = Depends(get_job_service)
) -> Any:
    with tracer.start_as_current_span("API.PATCH./api/v1/jobs/{id}"):
        job = await service.update_status(id, request.status, request.error_message)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

@router.post("/{id}/execute")
async def execute_job(current_user: UserModel = Depends(get_current_user), 
    id: UUID,
    service: BackgroundJobService = Depends(get_job_service)
) -> Any:
    with tracer.start_as_current_span("API.POST./api/v1/jobs/{id}/execute"):
        from src.infrastructure.workers.local_worker import execute_resume_extraction_job
        job = await service.get_job(id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.job_type == "resume_extraction":
            await execute_resume_extraction_job(id)
        else:
            raise HTTPException(status_code=400, detail="Unsupported job type")
        return {"status": "executed"}

class JobRequirementCreate(BaseModel):
    title: str
    description: str
    skills_required: list[str] = []
    experience_required: Optional[str] = None

@router.post("/requirements")
async def create_job_requirement(current_user: UserModel = Depends(get_current_user), 
    request: JobRequirementCreate,
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    with tracer.start_as_current_span("API.POST./api/v1/jobs/requirements"):
        from src.domain.entities import JobRequirement
        import uuid
        from datetime import datetime
        from src.infrastructure.database.repositories.job_requirement_repository import JobRequirementRepository
        from src.domain.enums import JobRequirementStatus
        
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
        from src.domain.enums import EmbeddingType
        import hashlib
        
        full_text = f"{created.title}\n\n{created.description}\n\n"
        full_text += "Skills:\n" + ", ".join(created.skills_required) + "\n\n"
        if created.experience_required:
            full_text += "Experience:\n" + created.experience_required
            
        from src.infrastructure.config import get_openai_api_key
        api_key = get_openai_api_key()
        embedding_provider = OpenAIEmbeddingProvider(api_key=api_key)
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
