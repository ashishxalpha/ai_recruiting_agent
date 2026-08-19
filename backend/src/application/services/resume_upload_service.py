from uuid import uuid4
from datetime import datetime
from typing import Dict, Any, List
import logging

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
from src.application.schemas.resumes import IngestionItemDTO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.database.models import (
    ResumeIngestionRequestModel,
    CandidateDocumentModel,
    BackgroundJobModel
)

tracer = get_tracer(__name__)
meter = get_meter(__name__)
logger = logging.getLogger(__name__)
upload_counter = meter.create_counter("resumes.uploaded", description="Number of resumes uploaded")

class ResumeUploadService:
    def __init__(
        self,
        document_repo: CandidateDocumentRepository,
        ingestion_repo: ResumeIngestionRequestRepository,
        job_repo: JobRepository,
        audit_repo: AuditRepository,
        storage_provider: StorageProvider,
        job_dispatcher: JobDispatcher,
        db_session: AsyncSession = None
    ):
        self.document_repo = document_repo
        self.ingestion_repo = ingestion_repo
        self.job_repo = job_repo
        self.audit_repo = audit_repo
        self.storage_provider = storage_provider
        self.job_dispatcher = job_dispatcher
        self.db_session = db_session

    async def get_recent_ingestions(self, limit: int = 10) -> List[IngestionItemDTO]:
        if not self.db_session:
            logger.warning("No db_session provided to ResumeUploadService for get_recent_ingestions")
            return []
            
        with tracer.start_as_current_span("ResumeUploadService.get_recent_ingestions"):
            # Join Ingestion, Document, and Job
            stmt = (
                select(ResumeIngestionRequestModel, CandidateDocumentModel, BackgroundJobModel)
                .join(CandidateDocumentModel, ResumeIngestionRequestModel.document_id == CandidateDocumentModel.id)
                .outerjoin(BackgroundJobModel, ResumeIngestionRequestModel.job_id == BackgroundJobModel.id)
                .order_by(ResumeIngestionRequestModel.created_at.desc())
                .limit(limit)
            )
            
            result = await self.db_session.execute(stmt)
            rows = result.all()
            
            dtos = []
            for ingestion, doc, job in rows:
                candidate_id = None
                error_message = None
                status = ingestion.status.value if ingestion.status else "PENDING"
                
                if job:
                    status = job.status.value
                    error_message = job.error_message
                    if job.result and isinstance(job.result, dict):
                        candidate_id_str = job.result.get("candidate_id")
                        if candidate_id_str:
                            import uuid
                            try:
                                candidate_id = uuid.UUID(candidate_id_str)
                            except ValueError:
                                pass
                                
                dtos.append(IngestionItemDTO(
                    id=ingestion.id,
                    filename=doc.original_name,
                    status=status,
                    created_at=ingestion.created_at,
                    candidate_id=candidate_id,
                    error_message=error_message
                ))
                
            return dtos

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
