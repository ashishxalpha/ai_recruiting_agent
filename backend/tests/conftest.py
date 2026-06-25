import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.main import app
from src.presentation.api.dependencies import (
    get_resume_upload_service,
    get_document_service,
    get_job_service,
    get_candidate_service
)
from src.domain.enums import JobStatus
from src.domain.entities import CandidateDocument, ResumeIngestionRequest, BackgroundJob, Candidate

@pytest.fixture
def mock_upload_service():
    service = AsyncMock()
    service.process_upload.return_value = {
        "ingestion_id": str(uuid4()),
        "document_id": str(uuid4()),
        "job_id": str(uuid4()),
        "status": JobStatus.QUEUED.value
    }
    return service

@pytest.fixture
def mock_document_service():
    service = AsyncMock()
    
    doc = CandidateDocument(id=uuid4(), file_path="path", file_type="application/pdf", original_name="test.pdf", storage_key="key", created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
    service.get_document.return_value = doc
    
    req = ResumeIngestionRequest(id=uuid4(), document_id=uuid4(), status=JobStatus.PENDING, created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
    service.get_document_status.return_value = req
    
    service.download_document.return_value = b"mock bytes"
    return service

@pytest.fixture
def mock_job_service():
    service = AsyncMock()
    job = BackgroundJob(id=uuid4(), job_type="test", correlation_id="123", status=JobStatus.QUEUED, payload={}, created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
    service.get_job.return_value = job
    service.update_status.return_value = job
    return service

@pytest.fixture
def mock_candidate_service():
    service = AsyncMock()
    c = Candidate(id=uuid4(), created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
    service.list_candidates.return_value = [c]
    service.get_candidate.return_value = c
    service.get_documents.return_value = []
    return service

@pytest.fixture
def client(mock_upload_service, mock_document_service, mock_job_service, mock_candidate_service):
    app.dependency_overrides[get_resume_upload_service] = lambda: mock_upload_service
    app.dependency_overrides[get_document_service] = lambda: mock_document_service
    app.dependency_overrides[get_job_service] = lambda: mock_job_service
    app.dependency_overrides[get_candidate_service] = lambda: mock_candidate_service
    
    with TestClient(app) as client:
        yield client
        
    app.dependency_overrides.clear()
