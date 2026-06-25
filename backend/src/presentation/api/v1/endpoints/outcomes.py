from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
import uuid

from src.presentation.api.dependencies import get_db
from src.domain.enums import GroundTruthEventType
from src.domain.entities import GroundTruthEvent
from src.infrastructure.database.repositories.ground_truth_repository import GroundTruthRepository
from src.infrastructure.events.event_bus import EventBus
from src.domain.events import GroundTruthRecorded

router = APIRouter()

class GroundTruthEventCreateRequest(BaseModel):
    candidate_id: UUID
    job_requirement_id: UUID
    event_type: GroundTruthEventType
    ai_score: float = 0.0
    recruiter_decision: Optional[str] = None

@router.post("/outcomes")
async def record_outcome(
    request: GroundTruthEventCreateRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Record a timeline event for candidate progression."""
    repo = GroundTruthRepository(db)
    
    event_entity = GroundTruthEvent(
        id=uuid.uuid4(),
        candidate_id=request.candidate_id,
        job_requirement_id=request.job_requirement_id,
        event_type=request.event_type,
        ai_score=request.ai_score,
        recruiter_decision=request.recruiter_decision,
        created_at=datetime.utcnow()
    )
    
    created = await repo.create(event_entity)
    await db.commit()

    domain_event = GroundTruthRecorded(
        event_id=uuid.uuid4(),
        occurred_at=datetime.utcnow(),
        candidate_id=created.candidate_id,
        job_requirement_id=created.job_requirement_id,
        event_type=created.event_type.value
    )
    EventBus.publish(domain_event)

    return created

@router.get("/outcomes/{event_id}")
async def get_outcome(
    event_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    repo = GroundTruthRepository(db)
    event = await repo.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Ground truth event not found")
    return event
