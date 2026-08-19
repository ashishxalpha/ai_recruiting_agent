from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from uuid import UUID
from typing import Any

from src.application.services.document_service import DocumentService
from src.presentation.api.dependencies import get_document_service, get_db_session
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

@router.get("/{id}")
async def get_document_metadata(
    id: UUID,
    service: DocumentService = Depends(get_document_service)
) -> Any:
    with tracer.start_as_current_span("API.GET./api/v1/documents/{id}"):
        doc = await service.get_document(id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc

@router.get("/{id}/status")
async def get_document_status(
    id: UUID,
    service: DocumentService = Depends(get_document_service),
    db: Any = Depends(get_db_session)
) -> Any:
    with tracer.start_as_current_span("API.GET./api/v1/documents/{id}/status"):
        status = await service.get_document_status(id)
        if not status:
            raise HTTPException(status_code=404, detail="Ingestion status not found")
        
        # Check actual background job status
        job = None
        if status.job_id:
            from sqlalchemy import select
            from src.infrastructure.database.models import BackgroundJobModel
            from src.domain.enums import JobStatus
            result = await db.execute(select(BackgroundJobModel).where(BackgroundJobModel.id == status.job_id))
            job = result.scalar_one_or_none()
            if job:
                status.status = job.status
                
        # We can append error_message to the dict if it's failed
        response_data = status.model_dump()
        if status.status == JobStatus.FAILED and job and job.error_message:
            response_data["error_message"] = job.error_message
            
        return response_data

@router.get("/{id}/download")
async def download_document(
    id: UUID,
    service: DocumentService = Depends(get_document_service)
):
    with tracer.start_as_current_span("API.GET./api/v1/documents/{id}/download"):
        doc = await service.get_document(id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
            
        file_bytes = await service.download_document(id)
        if not file_bytes:
            raise HTTPException(status_code=404, detail="File bytes not found in storage")
            
        return Response(content=file_bytes, media_type=doc.file_type)

@router.get("/{id}/metadata")
async def get_document_metadata_alias(
    id: UUID,
    service: DocumentService = Depends(get_document_service)
) -> Any:
    return await get_document_metadata(id, service)
