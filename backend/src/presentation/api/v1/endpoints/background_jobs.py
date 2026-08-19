from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import Any, Optional
from pydantic import BaseModel

from src.domain.enums import JobStatus
from src.application.services.job_service import BackgroundJobService
from src.presentation.api.dependencies import get_job_service
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

class JobUpdateRequest(BaseModel):
    status: JobStatus
    error_message: Optional[str] = None

@router.get("/{id}")
async def get_job(
    id: UUID,
    service: BackgroundJobService = Depends(get_job_service)
) -> Any:
    with tracer.start_as_current_span("API.GET./api/v1/background-jobs/{id}"):
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
    with tracer.start_as_current_span("API.PATCH./api/v1/background-jobs/{id}"):
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
    with tracer.start_as_current_span("API.POST./api/v1/background-jobs/{id}/execute"):
        from src.infrastructure.workers.local_worker import execute_resume_extraction_job
        job = await service.get_job(id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.job_type == "resume_extraction":
            await execute_resume_extraction_job(id)
        else:
            raise HTTPException(status_code=400, detail="Unsupported job type")
            
        return {"status": "executed"}
