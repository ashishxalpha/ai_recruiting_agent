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
        job_dispatcher=FastAPIJobDispatcher(background_tasks)
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

def get_workflow_engine(session: AsyncSession = fastapi.Depends(get_db_session)):
    from src.application.workflows.workflow_registry import InMemoryWorkflowDefinitionRegistry
    from src.infrastructure.workflows.langgraph_engine import LangGraphWorkflowEngine
    from src.infrastructure.workflows.checkpoints.database import DatabaseCheckpointStore
    
    registry = InMemoryWorkflowDefinitionRegistry()
    
    # We mock the node registry for Phase 2
    class MockNodeRegistry:
        def get_node(self, node_name: str):
            from src.application.workflows.interfaces import WorkflowNode, NodeRetryPolicy
            from src.application.workflows.state import RecruitingWorkflowState
            
            class MockNode(WorkflowNode):
                @property
                def retry_policy(self):
                    return None
                async def execute(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
                    return state
                async def rollback(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
                    return state
                    
            return MockNode()
            
        def register_node(self, node_name: str, node):
            pass
            
    from src.infrastructure.workflows.definitions.recruiting import RecruitingLangGraphDefinition
    registry.register(RecruitingLangGraphDefinition(MockNodeRegistry()))
    
    checkpointer = DatabaseCheckpointStore(session)
    return LangGraphWorkflowEngine(registry, checkpointer, session)
