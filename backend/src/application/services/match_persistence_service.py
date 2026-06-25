from typing import List
import uuid
from datetime import datetime
from src.domain.entities import CandidateMatchResult, SearchSession, CandidateMatch, MatchExplanation
from src.infrastructure.database.repositories.search_session_repository import SearchSessionRepository
from src.infrastructure.database.repositories.candidate_match_repository import CandidateMatchRepository
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class CandidateMatchPersistenceService:
    def __init__(self, session_repo: SearchSessionRepository, match_repo: CandidateMatchRepository):
        self.session_repo = session_repo
        self.match_repo = match_repo

    async def persist_matches(self, job_requirement_id: uuid.UUID, results: List[CandidateMatchResult]) -> uuid.UUID:
        with tracer.start_as_current_span("CandidateMatchPersistenceService.persist_matches"):
            # 1. Create a new Search Session
            session_id = uuid.uuid4()
            session = SearchSession(
                id=session_id,
                job_requirement_id=job_requirement_id,
                created_at=datetime.utcnow()
            )
            await self.session_repo.create(session)

            # 2. Persist Matches and Explanations
            matches = []
            explanations = []

            for res in results:
                match_id = uuid.uuid4()
                # Update DTO to include session id
                res.search_session_id = session_id
                
                match = CandidateMatch(
                    id=match_id,
                    search_session_id=session_id,
                    candidate_id=res.candidate_id,
                    semantic_score=res.semantic_score,
                    skills_score=res.skills_score,
                    experience_score=res.experience_score,
                    education_score=res.education_score,
                    quality_score=0.0, # Computed separately or mapped from result
                    final_score=res.final_score,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                matches.append(match)

                explanation = MatchExplanation(
                    id=uuid.uuid4(),
                    candidate_match_id=match_id,
                    explanation_version="v1",
                    strengths=res.strengths,
                    gaps=res.gaps,
                    recommendations=res.recommendations,
                    created_at=datetime.utcnow()
                )
                explanations.append(explanation)

            if matches:
                await self.match_repo.create_matches_batch(matches, explanations)

            # Emit Domain Event (CandidateMatched) handled by caller or here
            # For simplicity, returning session_id, caller will emit event

            return session_id
