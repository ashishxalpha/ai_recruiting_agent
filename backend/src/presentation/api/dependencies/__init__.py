import fastapi
from fastapi import Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.infrastructure.database.base import get_session
from src.infrastructure.database.repositories.document_repository import SQLAlchemyCandidateDocumentRepository
from src.infrastructure.database.repositories.ingestion_repository import SQLAlchemyResumeIngestionRequestRepository
from src.infrastructure.database.repositories.job_repository import SQLAlchemyJobRepository
from src.infrastructure.database.repositories.audit_repository import SQLAlchemyAuditRepository
from src.infrastructure.database.repositories.candidate_repository import SQLAlchemyCandidateRepository
from src.infrastructure.providers.storage.local import LocalStorageProvider
from src.infrastructure.providers.jobs.fastapi_dispatcher import FastAPIJobDispatcher

from src.application.services.resume_upload_service import ResumeUploadService
from src.application.services.document_service import DocumentService
from src.application.services.job_service import BackgroundJobService
from src.application.services.candidate_service import CandidateService

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session

def get_storage_provider() -> LocalStorageProvider:
    return LocalStorageProvider(base_path="/storage")

def get_job_dispatcher(background_tasks: BackgroundTasks) -> FastAPIJobDispatcher:
    return FastAPIJobDispatcher(background_tasks=background_tasks)

def get_resume_upload_service(
    background_tasks: BackgroundTasks,
    session: AsyncSession = fastapi.Depends(get_db_session),
    storage_provider: LocalStorageProvider = fastapi.Depends(get_storage_provider),
) -> ResumeUploadService:
    return ResumeUploadService(
        document_repo=SQLAlchemyCandidateDocumentRepository(session),
        ingestion_repo=SQLAlchemyResumeIngestionRequestRepository(session),
        job_repo=SQLAlchemyJobRepository(session),
        audit_repo=SQLAlchemyAuditRepository(session),
        storage_provider=storage_provider,
        job_dispatcher=FastAPIJobDispatcher(background_tasks),
        db_session=session
    )

def get_document_service(
    session: AsyncSession = fastapi.Depends(get_db_session),
    storage_provider: LocalStorageProvider = fastapi.Depends(get_storage_provider)
) -> DocumentService:
    return DocumentService(
        document_repo=SQLAlchemyCandidateDocumentRepository(session),
        ingestion_repo=SQLAlchemyResumeIngestionRequestRepository(session),
        storage_provider=storage_provider
    )

def get_job_service(session: AsyncSession = fastapi.Depends(get_db_session)) -> BackgroundJobService:
    return BackgroundJobService(job_repo=SQLAlchemyJobRepository(session))

def get_candidate_service(session: AsyncSession = fastapi.Depends(get_db_session)) -> CandidateService:
    return CandidateService(
        candidate_repo=SQLAlchemyCandidateRepository(session),
        document_repo=SQLAlchemyCandidateDocumentRepository(session)
    )

def get_candidate_matching_service(session: AsyncSession = fastapi.Depends(get_db_session)):
    import os
    from src.infrastructure.providers.ai.openai import OpenAIExtractionProvider
    from src.infrastructure.database.repositories.search_session_repository import SearchSessionRepository
    from src.infrastructure.database.repositories.candidate_match_repository import CandidateMatchRepository
    from src.application.services.match_persistence_service import CandidateMatchPersistenceService
    from src.application.services.candidate_matching_service import CandidateMatchingService
    
    api_key = os.getenv("OPENAI_API_KEY", "dummy_key")
    model_name = os.getenv("AI_EXTRACTION_MODEL", "gpt-4o")
    ai_provider = OpenAIExtractionProvider(api_key=api_key, model_name=model_name)
    
    session_repo = SearchSessionRepository(session)
    match_repo = CandidateMatchRepository(session)
    persistence_service = CandidateMatchPersistenceService(session_repo, match_repo)
    
    return CandidateMatchingService(session, ai_provider, persistence_service)

def get_workflow_engine(session: AsyncSession = fastapi.Depends(get_db_session)):
    from src.application.workflows.workflow_registry import InMemoryWorkflowDefinitionRegistry
    from src.infrastructure.workflows.langgraph_engine import LangGraphWorkflowEngine
    from src.infrastructure.workflows.checkpoints.database import DatabaseCheckpointStore
    
    registry = InMemoryWorkflowDefinitionRegistry()
    
    from src.infrastructure.workflows.nodes.registry import RealNodeRegistry
    
    registry.register(RecruitingLangGraphDefinition(RealNodeRegistry()))
    
    checkpointer = DatabaseCheckpointStore(session)
    return LangGraphWorkflowEngine(registry, checkpointer, session)
