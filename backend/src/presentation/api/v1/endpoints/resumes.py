from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from src.application.services.resume_upload_service import ResumeUploadService
from src.presentation.api.dependencies import get_resume_upload_service
from src.observability.tracing import get_tracer

router = APIRouter()
tracer = get_tracer(__name__)

class UploadResponse(BaseModel):
    ingestion_id: str
    document_id: str
    job_id: str
    status: str

ALLOWED_MIME_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(
    file: UploadFile = File(...),
    upload_service: ResumeUploadService = Depends(get_resume_upload_service)
):
    with tracer.start_as_current_span("API.POST./api/v1/resumes/upload"):
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are allowed.")
        
        file_bytes = await file.read()
        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
        
        result = await upload_service.process_upload(file_bytes, file.filename, file.content_type)
        return UploadResponse(**result)
