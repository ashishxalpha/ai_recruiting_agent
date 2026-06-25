from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Optional, List

from src.domain.entities import GroundTruthEvent
from src.infrastructure.database.models import GroundTruthEventModel

class GroundTruthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event: GroundTruthEvent) -> GroundTruthEvent:
        model = GroundTruthEventModel(
            id=event.id,
            candidate_id=event.candidate_id,
            job_requirement_id=event.job_requirement_id,
            event_type=event.event_type,
            ai_score=event.ai_score,
            recruiter_decision=event.recruiter_decision,
            created_at=event.created_at
        )
        self.session.add(model)
        await self.session.flush()
        return event

    async def get_by_id(self, id: UUID) -> Optional[GroundTruthEvent]:
        stmt = select(GroundTruthEventModel).where(GroundTruthEventModel.id == id)
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()
        if not model:
            return None
        return GroundTruthEvent(
            id=model.id,
            candidate_id=model.candidate_id,
            job_requirement_id=model.job_requirement_id,
            event_type=model.event_type,
            ai_score=model.ai_score,
            recruiter_decision=model.recruiter_decision,
            created_at=model.created_at
        )

    async def get_timeline_for_candidate(self, candidate_id: UUID, job_id: UUID) -> List[GroundTruthEvent]:
        stmt = (
            select(GroundTruthEventModel)
            .where(
                GroundTruthEventModel.candidate_id == candidate_id,
                GroundTruthEventModel.job_requirement_id == job_id
            )
            .order_by(GroundTruthEventModel.created_at.asc())
        )
        res = await self.session.execute(stmt)
        models = res.scalars().all()
        return [
            GroundTruthEvent(
                id=m.id,
                candidate_id=m.candidate_id,
                job_requirement_id=m.job_requirement_id,
                event_type=m.event_type,
                ai_score=m.ai_score,
                recruiter_decision=m.recruiter_decision,
                created_at=m.created_at
            ) for m in models
        ]
