from uuid import uuid4
from datetime import datetime
from typing import Dict, Any

from src.domain.entities import CandidateDocument, ResumeIngestionRequest, BackgroundJob
from src.domain.enums import JobStatus
from src.domain.interfaces.repositories import (
    CandidateDocumentRepository,
    ResumeIngestionRequestRepository,
    JobRepository,
    AuditRepository
)
from src.domain.interfaces.providers import StorageProvider, JobDispatcher
from src.observability.tracing import get_tracer
from src.observability.metrics import get_meter

tracer = get_tracer(__name__)
meter = get_meter(__name__)
upload_counter = meter.create_counter("resumes.uploaded", description="Number of resumes uploaded")

class ResumeUploadService:
    def __init__(
        self,
        document_repo: CandidateDocumentRepository,
        ingestion_repo: ResumeIngestionRequestRepository,
        job_repo: JobRepository,
        audit_repo: AuditRepository,
        storage_provider: StorageProvider,
        job_dispatcher: JobDispatcher
    ):
        self.document_repo = document_repo
        self.ingestion_repo = ingestion_repo
        self.job_repo = job_repo
        self.audit_repo = audit_repo
        self.storage_provider = storage_provider
        self.job_dispatcher = job_dispatcher

    async def process_upload(self, file_bytes: bytes, filename: str, content_type: str) -> Dict[str, Any]:
        with tracer.start_as_current_span("ResumeUploadService.process_upload") as span:
            span.set_attribute("file.name", filename)
            span.set_attribute("file.size", len(file_bytes))
            span.set_attribute("file.type", content_type)

            # 1. Upload to storage
            storage_key = await self.storage_provider.upload(file_bytes, filename, category="candidate-documents")
            
            # 2. Create CandidateDocument
            doc_id = uuid4()
            now = datetime.utcnow()
            document = CandidateDocument(
                id=doc_id,
                file_path=f"/candidate-documents/{filename}",
                file_type=content_type,
                original_name=filename,
                storage_key=storage_key,
                created_at=now,
                updated_at=now
            )
            await self.document_repo.create(document)
            
            # 3. Create BackgroundJob
            job_id = uuid4()
            job = BackgroundJob(
                id=job_id,
                job_type="resume_extraction",
                correlation_id=str(doc_id),
                status=JobStatus.QUEUED,
                payload={"document_id": str(doc_id), "storage_key": storage_key},
                created_at=now,
                updated_at=now
            )
            await self.job_repo.create(job)
            
            # 4. Create ResumeIngestionRequest
            ingestion_id = uuid4()
            ingestion_request = ResumeIngestionRequest(
                id=ingestion_id,
                document_id=doc_id,
                job_id=job_id,
                status=JobStatus.QUEUED,
                created_at=now,
                updated_at=now
            )
            await self.ingestion_repo.create(ingestion_request)
            
            # 5. Audit Log
            await self.audit_repo.log_action(
                entity_type="ResumeIngestionRequest",
                entity_id=ingestion_id,
                action="UPLOADED",
                changes={"document_id": str(doc_id), "job_id": str(job_id)}
            )
            
            # 6. Dispatch Job
            await self.job_dispatcher.dispatch("resume_extraction", {"job_id": str(job_id)})
            
            upload_counter.add(1)
            
            return {
                "ingestion_id": str(ingestion_id),
                "document_id": str(doc_id),
                "job_id": str(job_id),
                "status": JobStatus.QUEUED.value
            }
