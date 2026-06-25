from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import Any, Optional
from pydantic import BaseModel

from src.domain.enums import JobStatus, JobRequirementStatus, EmbeddingType
from src.application.services.job_service import BackgroundJobService
from src.presentation.api.dependencies import get_job_service, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

class JobRequirementCreate(BaseModel):
    title: str
    description: str
    skills_required: list[str] = []
    experience_required: Optional[str] = None

class JobUpdateRequest(BaseModel):
    status: JobStatus
    error_message: Optional[str] = None

@router.get("/{id}")
async def get_job(
    id: UUID,
    service: BackgroundJobService = Depends(get_job_service)
) -> Any:
    with tracer.start_as_current_span("API.GET./api/v1/jobs/{id}"):
        job = await service.get_job(id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

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
async def execute_job(
    id: UUID,
    service: BackgroundJobService = Depends(get_job_service)
) -> Any:
    """Manually execute a background job for development purposes."""
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

@router.post("/requirements")
async def create_job_requirement(
    request: JobRequirementCreate,
    db: AsyncSession = Depends(get_db)
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
