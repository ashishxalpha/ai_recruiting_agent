from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List, Optional

from src.domain.entities import CandidateMatch, MatchExplanation
from src.infrastructure.database.models import CandidateMatchModel, MatchExplanationModel

class CandidateMatchRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_match(self, match: CandidateMatch, explanation: MatchExplanation) -> None:
        match_model = CandidateMatchModel(
            id=match.id,
            search_session_id=match.search_session_id,
            candidate_id=match.candidate_id,
            semantic_score=match.semantic_score,
            skills_score=match.skills_score,
            experience_score=match.experience_score,
            education_score=match.education_score,
            quality_score=match.quality_score,
            final_score=match.final_score,
            created_at=match.created_at,
            updated_at=match.updated_at
        )
        self.session.add(match_model)

        exp_model = MatchExplanationModel(
            id=explanation.id,
            candidate_match_id=explanation.candidate_match_id,
            explanation_version=explanation.explanation_version,
            strengths=explanation.strengths,
            gaps=explanation.gaps,
            recommendations=explanation.recommendations,
            created_at=explanation.created_at
        )
        self.session.add(exp_model)
        await self.session.flush()

    async def create_matches_batch(self, matches: List[CandidateMatch], explanations: List[MatchExplanation]) -> None:
        match_models = [
            CandidateMatchModel(
                id=m.id, search_session_id=m.search_session_id, candidate_id=m.candidate_id,
                semantic_score=m.semantic_score, skills_score=m.skills_score,
                experience_score=m.experience_score, education_score=m.education_score,
                quality_score=m.quality_score, final_score=m.final_score,
                created_at=m.created_at, updated_at=m.updated_at
            ) for m in matches
        ]
        self.session.add_all(match_models)

        exp_models = [
            MatchExplanationModel(
                id=e.id, candidate_match_id=e.candidate_match_id,
                explanation_version=e.explanation_version, strengths=e.strengths,
                gaps=e.gaps, recommendations=e.recommendations, created_at=e.created_at
            ) for e in explanations
        ]
        self.session.add_all(exp_models)
        await self.session.flush()

    async def get_match_by_id(self, match_id: UUID) -> Optional[CandidateMatch]:
        stmt = select(CandidateMatchModel).where(CandidateMatchModel.id == match_id)
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()
        if not model:
            return None
        return CandidateMatch(
            id=model.id, search_session_id=model.search_session_id, candidate_id=model.candidate_id,
            semantic_score=model.semantic_score, skills_score=model.skills_score,
            experience_score=model.experience_score, education_score=model.education_score,
            quality_score=model.quality_score, final_score=model.final_score,
            created_at=model.created_at, updated_at=model.updated_at
        )
