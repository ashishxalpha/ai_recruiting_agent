from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from uuid import UUID

from src.application.schemas.feedback import PendingMatchDTO, FeedbackCreateRequest
from src.infrastructure.database.models import (
    CandidateMatchModel,
    CandidateModel,
    SearchSessionModel,
    JobRequirementModel,
    RecruiterFeedbackModel
)

class FeedbackService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pending_feedback(self) -> List[PendingMatchDTO]:
        # Get matches that do not have feedback yet
        # Using a left outer join to RecruiterFeedbackModel and filtering where it's NULL
        stmt = (
            select(CandidateMatchModel, CandidateModel, JobRequirementModel)
            .join(CandidateModel, CandidateModel.id == CandidateMatchModel.candidate_id)
            .join(SearchSessionModel, SearchSessionModel.id == CandidateMatchModel.search_session_id)
            .join(JobRequirementModel, JobRequirementModel.id == SearchSessionModel.job_requirement_id)
            .outerjoin(RecruiterFeedbackModel, RecruiterFeedbackModel.candidate_match_id == CandidateMatchModel.id)
            .where(RecruiterFeedbackModel.id == None)
            .order_by(desc(CandidateMatchModel.final_score))
            .limit(50)
        )
        
        result = await self.session.execute(stmt)
        rows = result.all()
        
        dtos = []
        for match, candidate, job in rows:
            dtos.append(PendingMatchDTO(
                id=match.id,
                candidate=f"{candidate.first_name or ''} {candidate.last_name or ''}".strip() or "Unknown",
                job=job.title,
                score=match.final_score,
                status="PENDING",
                created_at=match.created_at
            ))
            
        return dtos

    async def submit_feedback(self, request: FeedbackCreateRequest) -> RecruiterFeedbackModel:
        feedback = RecruiterFeedbackModel(
            candidate_match_id=request.candidate_match_id,
            decision=request.decision,
            confidence=request.confidence,
            reason=request.reason,
            notes=request.notes
        )
        
        self.session.add(feedback)
        await self.session.commit()
        await self.session.refresh(feedback)
        
        return feedback
