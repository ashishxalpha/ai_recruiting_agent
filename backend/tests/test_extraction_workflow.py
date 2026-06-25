import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime

from src.application.jobs.resume_extraction import ResumeExtractionWorkflow
from src.domain.entities import BackgroundJob, CandidateDocument, Candidate
from src.domain.enums import JobStatus, CandidateStatus
from src.application.schemas.extraction import CandidateProfile, Skill
from src.application.schemas.evaluation import ProfileEvaluationResult
from src.infrastructure.parsers.base import DocumentContent

@pytest.fixture
def mock_deps():
    return {
        "job_repo": AsyncMock(),
        "document_repo": AsyncMock(),
        "candidate_repo": AsyncMock(),
        "extraction_repo": AsyncMock(),
        "storage_provider": AsyncMock(),
        "ai_provider": AsyncMock(),
        "dlq_provider": AsyncMock(),
        "validator": MagicMock(),
        "evaluator": MagicMock()
    }

@pytest.mark.asyncio
async def test_workflow_success(mock_deps):
    workflow = ResumeExtractionWorkflow(**mock_deps)
    job_id = uuid4()
    doc_id = uuid4()
    
    # Setup job
    job = BackgroundJob(
        id=job_id, job_type="resume_extraction", correlation_id=str(doc_id),
        status=JobStatus.PENDING, payload={"document_id": str(doc_id)}, created_at=datetime.utcnow(), updated_at=datetime.utcnow()
    )
    mock_deps["job_repo"].get_by_id.return_value = job
    
    # Setup document
    doc = CandidateDocument(
        id=doc_id, file_path="/fake", file_type="application/pdf", original_name="test.pdf",
        storage_key="test_key", created_at=datetime.utcnow(), updated_at=datetime.utcnow()
    )
    mock_deps["document_repo"].get_by_id.return_value = doc
    
    # Setup storage & parser
    mock_deps["storage_provider"].get_file.return_value = b"fake pdf bytes"
    
    # We will patch PDFParser
    with pytest.MonkeyPatch.context() as m:
        class FakeParser:
            def parse(self, b):
                return DocumentContent(text="parsed resume text", page_count=1, metadata={})
        m.setattr("src.application.jobs.resume_extraction.PDFParser", FakeParser)
        
        # Setup AI Provider
        profile = CandidateProfile(first_name="Jane", last_name="Smith", skills=[Skill(name="Python")])
        metrics = {"provider": "test", "model_name": "test", "input_tokens": 10, "output_tokens": 10, "total_tokens": 20, "processing_time_ms": 100, "raw_response": {}}
        mock_deps["ai_provider"].extract_profile.return_value = (profile, metrics)
        
        # Setup Validator & Evaluator
        mock_deps["validator"].validate.return_value = profile
        mock_deps["evaluator"].evaluate.return_value = ProfileEvaluationResult(
            confidence_score=0.9, completeness_score=0.9, quality_score=0.9, warnings=[], issues=[]
        )
        
        # Execute
        await workflow.execute(job_id)
        
        # Verify job status updated
        assert job.status == JobStatus.COMPLETED
        assert job.result is not None
        mock_deps["job_repo"].update.assert_called()
        
        # Verify extraction stored
        mock_deps["extraction_repo"].create.assert_called_once()
        extraction = mock_deps["extraction_repo"].create.call_args[0][0]
        assert extraction.overall_confidence == 0.9
        
        # Verify candidate created
        mock_deps["candidate_repo"].create.assert_called_once()
        candidate = mock_deps["candidate_repo"].create.call_args[0][0]
        assert candidate.first_name == "Jane"
        assert candidate.status == CandidateStatus.UNDER_REVIEW
        assert len(candidate.skills) == 1

@pytest.mark.asyncio
async def test_workflow_fails(mock_deps):
    workflow = ResumeExtractionWorkflow(**mock_deps)
    job_id = uuid4()
    
    # Setup job
    job = BackgroundJob(
        id=job_id, job_type="resume_extraction", correlation_id="x",
        status=JobStatus.PENDING, payload={"document_id": str(uuid4())}, created_at=datetime.utcnow(), updated_at=datetime.utcnow()
    )
    mock_deps["job_repo"].get_by_id.return_value = job
    mock_deps["document_repo"].get_by_id.return_value = None  # Document missing -> triggers failure
    
    await workflow.execute(job_id)
    
    assert job.status == JobStatus.FAILED
    assert "not found" in job.error_message
    
    # DLQ tracked
    mock_deps["dlq_provider"].track_failure.assert_called_once()
