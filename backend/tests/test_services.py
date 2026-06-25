import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.application.services.resume_upload_service import ResumeUploadService
from src.application.services.document_service import DocumentService
from src.application.services.job_service import BackgroundJobService
from src.application.services.candidate_service import CandidateService
from src.domain.enums import JobStatus
from src.domain.entities import CandidateDocument, ResumeIngestionRequest, BackgroundJob

@pytest.mark.asyncio
async def test_process_upload():
    doc_repo = AsyncMock()
    ingest_repo = AsyncMock()
    job_repo = AsyncMock()
    audit_repo = AsyncMock()
    storage = AsyncMock()
    storage.upload.return_value = "storage/key.pdf"
    dispatcher = AsyncMock()
    
    service = ResumeUploadService(
        document_repo=doc_repo,
        ingestion_repo=ingest_repo,
        job_repo=job_repo,
        audit_repo=audit_repo,
        storage_provider=storage,
        job_dispatcher=dispatcher
    )
    
    res = await service.process_upload(b"test", "test.pdf", "application/pdf")
    
    assert "document_id" in res
    assert "job_id" in res
    
    storage.upload.assert_called_once()
    doc_repo.create.assert_called_once()
    ingest_repo.create.assert_called_once()
    job_repo.create.assert_called_once()
    audit_repo.log_action.assert_called_once()
    dispatcher.dispatch.assert_called_once()

@pytest.mark.asyncio
async def test_document_service():
    doc_repo = AsyncMock()
    ingest_repo = AsyncMock()
    storage = AsyncMock()
    
    doc = CandidateDocument(id=uuid4(), file_path="", file_type="", original_name="", storage_key="", created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
    req = ResumeIngestionRequest(id=uuid4(), document_id=uuid4(), created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
    
    doc_repo.get_by_id.return_value = doc
    ingest_repo.get_by_document_id.return_value = req
    storage.download.return_value = b"test"
    
    service = DocumentService(doc_repo, ingest_repo, storage)
    
    res1 = await service.get_document(uuid4())
    assert res1 == doc
    
    res2 = await service.get_document_status(uuid4())
    assert res2 == req
    
    res3 = await service.download_document(uuid4())
    assert res3 == b"test"
    
    doc_repo.get_by_id.return_value = None
    res4 = await service.download_document(uuid4())
    assert res4 is None

@pytest.mark.asyncio
async def test_job_service():
    job_repo = AsyncMock()
    job = BackgroundJob(id=uuid4(), job_type="a", correlation_id="b", payload={}, created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
    job_repo.get_by_id.return_value = job
    job_repo.update.return_value = job
    
    service = BackgroundJobService(job_repo)
    
    res1 = await service.get_job(uuid4())
    assert res1 == job
    
    res2 = await service.update_status(uuid4(), JobStatus.COMPLETED, "error")
    assert res2.status == JobStatus.COMPLETED
    assert res2.error_message == "error"
    
    job_repo.get_by_id.return_value = None
    res3 = await service.update_status(uuid4(), JobStatus.COMPLETED)
    assert res3 is None

@pytest.mark.asyncio
async def test_candidate_service():
    cand_repo = AsyncMock()
    doc_repo = AsyncMock()
    cand_repo.get_all.return_value = ["c1"]
    cand_repo.get_by_id.return_value = "c1"
    doc_repo.get_by_candidate_id.return_value = ["d1"]
    
    service = CandidateService(cand_repo, doc_repo)
    
    res1 = await service.list_candidates()
    assert res1 == ["c1"]
    
    res2 = await service.get_candidate(uuid4())
    assert res2 == "c1"
    
    res3 = await service.get_documents(uuid4())
    assert res3 == ["d1"]
