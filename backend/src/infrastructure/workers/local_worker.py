import uuid
import os
import logging
from src.infrastructure.database.base import async_session_maker
from src.infrastructure.database.repositories.job_repository import SQLAlchemyJobRepository
from src.infrastructure.database.repositories.document_repository import SQLAlchemyCandidateDocumentRepository
from src.infrastructure.database.repositories.candidate_repository import SQLAlchemyCandidateRepository
from src.infrastructure.database.repositories.ai_extraction_repository import SQLAlchemyAIExtractionRepository
from src.infrastructure.providers.storage.local import LocalStorageProvider
from src.infrastructure.providers.ai.openai import OpenAIExtractionProvider
from src.application.services.validation import CandidateProfileValidator
from src.application.services.evaluation import ProfileEvaluator
from src.domain.interfaces.dlq import FailedExtractionTrackingProvider
from src.application.jobs.resume_extraction import ResumeExtractionWorkflow
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)
logger = logging.getLogger(__name__)

from src.infrastructure.database.repositories.audit_repository import SQLAlchemyAuditRepository

class DatabaseDLQProvider(FailedExtractionTrackingProvider):
    def __init__(self, session):
        self.session = session
        
    async def track_failure(self, document_id, error_type, error_message, payload=None):
        logger.error(f"DLQ: Failed extraction for document {document_id}. {error_type}: {error_message}")
        audit_repo = SQLAlchemyAuditRepository(self.session)
        await audit_repo.log_action(
            entity_type="document_extraction_dlq",
            entity_id=document_id or uuid.uuid4(),
            action="extraction_failed",
            changes={"error_type": error_type, "error_message": error_message, "payload": payload}
        )
        
    async def get_failed_extractions(self, limit=100, offset=0):
        return []

async def execute_resume_extraction_job(job_id: uuid.UUID):
    """
    Executes the resume extraction workflow. Designed to be run by a background task.
    """
    with tracer.start_as_current_span("execute_resume_extraction_job"):
        async with async_session_maker() as session:
            try:
                job_repo = SQLAlchemyJobRepository(session)
                document_repo = SQLAlchemyCandidateDocumentRepository(session)
                candidate_repo = SQLAlchemyCandidateRepository(session)
                extraction_repo = SQLAlchemyAIExtractionRepository(session)
                
                storage_provider = LocalStorageProvider("/storage")
                
                from src.infrastructure.providers.embedding.openai import OpenAIEmbeddingProvider
                from src.infrastructure.database.repositories.embedding_repository import CandidateEmbeddingRepository
                
                api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
                extraction_model = os.getenv("AI_EXTRACTION_MODEL", "gpt-4o-2024-08-06")
                embedding_model = os.getenv("AI_EMBEDDING_MODEL", "text-embedding-3-small")
                ai_provider = OpenAIExtractionProvider(api_key=api_key, model_name=extraction_model)
                embedding_provider = OpenAIEmbeddingProvider(api_key=api_key, model=embedding_model)
                
                dlq_provider = DatabaseDLQProvider(session)
                validator = CandidateProfileValidator()
                evaluator = ProfileEvaluator()
                embedding_repo = CandidateEmbeddingRepository(session)
                
                workflow = ResumeExtractionWorkflow(
                    job_repo=job_repo,
                    document_repo=document_repo,
                    candidate_repo=candidate_repo,
                    extraction_repo=extraction_repo,
                    storage_provider=storage_provider,
                    ai_provider=ai_provider,
                    dlq_provider=dlq_provider,
                    validator=validator,
                    evaluator=evaluator,
                    embedding_provider=embedding_provider,
                    embedding_repo=embedding_repo
                )
                
                await workflow.execute(job_id)
                await session.commit()
            except Exception as e:
                logger.exception(f"Failed to execute background job {job_id}: {e}")
                await session.rollback()
