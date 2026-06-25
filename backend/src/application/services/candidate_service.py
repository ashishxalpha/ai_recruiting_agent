from uuid import UUID
from typing import Optional, List

from src.domain.entities import Candidate, CandidateDocument
from src.domain.interfaces.repositories import CandidateRepository, CandidateDocumentRepository
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class CandidateService:
    def __init__(self, candidate_repo: CandidateRepository, document_repo: CandidateDocumentRepository):
        self.candidate_repo = candidate_repo
        self.document_repo = document_repo

    async def list_candidates(self, skip: int = 0, limit: int = 100) -> List[Candidate]:
        with tracer.start_as_current_span("CandidateService.list_candidates"):
            return await self.candidate_repo.get_all(skip, limit)

    async def get_candidate(self, candidate_id: UUID) -> Optional[Candidate]:
        with tracer.start_as_current_span("CandidateService.get_candidate"):
            return await self.candidate_repo.get_by_id(candidate_id)

    async def get_documents(self, candidate_id: UUID) -> List[CandidateDocument]:
        with tracer.start_as_current_span("CandidateService.get_documents"):
            return await self.document_repo.get_by_candidate_id(candidate_id)
