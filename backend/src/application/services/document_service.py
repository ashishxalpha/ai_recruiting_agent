from uuid import UUID
from typing import Optional

from src.domain.entities import CandidateDocument, ResumeIngestionRequest
from src.domain.interfaces.repositories import CandidateDocumentRepository, ResumeIngestionRequestRepository
from src.domain.interfaces.providers import StorageProvider
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class DocumentService:
    def __init__(
        self,
        document_repo: CandidateDocumentRepository,
        ingestion_repo: ResumeIngestionRequestRepository,
        storage_provider: StorageProvider
    ):
        self.document_repo = document_repo
        self.ingestion_repo = ingestion_repo
        self.storage_provider = storage_provider

    async def get_document(self, document_id: UUID) -> Optional[CandidateDocument]:
        with tracer.start_as_current_span("DocumentService.get_document"):
            return await self.document_repo.get_by_id(document_id)

    async def get_document_status(self, document_id: UUID) -> Optional[ResumeIngestionRequest]:
        with tracer.start_as_current_span("DocumentService.get_document_status"):
            return await self.ingestion_repo.get_by_document_id(document_id)

    async def download_document(self, document_id: UUID) -> Optional[bytes]:
        with tracer.start_as_current_span("DocumentService.download_document"):
            document = await self.document_repo.get_by_id(document_id)
            if not document:
                return None
            return await self.storage_provider.download(document.storage_key)
