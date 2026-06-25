from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
from typing import Optional

from src.domain.entities import RecruiterFeedback
from src.infrastructure.database.models import RecruiterFeedbackModel

class RecruiterFeedbackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, feedback: RecruiterFeedback) -> RecruiterFeedback:
        model = RecruiterFeedbackModel(
            id=feedback.id,
            candidate_match_id=feedback.candidate_match_id,
            decision=feedback.decision,
            confidence=feedback.confidence,
            reason=feedback.reason,
            notes=feedback.notes,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at
        )
        self.session.add(model)
        await self.session.flush()
        return feedback

    async def get_by_id(self, id: UUID) -> Optional[RecruiterFeedback]:
        stmt = select(RecruiterFeedbackModel).where(RecruiterFeedbackModel.id == id)
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()
        if not model:
            return None
        return RecruiterFeedback(
            id=model.id,
            candidate_match_id=model.candidate_match_id,
            decision=model.decision,
            confidence=model.confidence,
            reason=model.reason,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_by_match_id(self, match_id: UUID) -> Optional[RecruiterFeedback]:
        stmt = select(RecruiterFeedbackModel).where(RecruiterFeedbackModel.candidate_match_id == match_id)
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()
        if not model:
            return None
        return RecruiterFeedback(
            id=model.id,
            candidate_match_id=model.candidate_match_id,
            decision=model.decision,
            confidence=model.confidence,
            reason=model.reason,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def update(self, feedback: RecruiterFeedback) -> RecruiterFeedback:
        stmt = (
            update(RecruiterFeedbackModel)
            .where(RecruiterFeedbackModel.id == feedback.id)
            .values(
                decision=feedback.decision,
                confidence=feedback.confidence,
                reason=feedback.reason,
                notes=feedback.notes,
                updated_at=feedback.updated_at
            )
        )
        await self.session.execute(stmt)
        await self.session.flush()
        return feedback
