from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from src.presentation.api.dependencies import get_db
from src.domain.enums import RecruiterDecision
from src.domain.entities import RecruiterFeedback
from src.infrastructure.database.repositories.feedback_repository import RecruiterFeedbackRepository
from src.infrastructure.events.event_bus import EventBus
from src.domain.events import RecruiterFeedbackSubmitted

router = APIRouter()

class FeedbackCreateRequest(BaseModel):
    decision: RecruiterDecision
    confidence: float = 1.0
    reason: Optional[str] = None
    notes: Optional[str] = None

class FeedbackUpdateRequest(BaseModel):
    decision: Optional[RecruiterDecision] = None
    confidence: Optional[float] = None
    reason: Optional[str] = None
    notes: Optional[str] = None

@router.post("/matches/{match_id}/feedback")
async def submit_feedback(
    match_id: UUID,
    request: FeedbackCreateRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Submit recruiter feedback for a specific candidate match."""
    import uuid
    repo = RecruiterFeedbackRepository(db)
    
    # Check if exists
    existing = await repo.get_by_match_id(match_id)
    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted for this match.")

    feedback = RecruiterFeedback(
        id=uuid.uuid4(),
        candidate_match_id=match_id,
        decision=request.decision,
        confidence=request.confidence,
        reason=request.reason,
        notes=request.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    created = await repo.create(feedback)
    await db.commit()

    event = RecruiterFeedbackSubmitted(
        event_id=uuid.uuid4(),
        occurred_at=datetime.utcnow(),
        feedback_id=created.id,
        candidate_match_id=match_id,
        decision=created.decision.value
    )
    EventBus.publish(event)

    return created

@router.get("/matches/{match_id}/feedback")
async def get_feedback(
    match_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    repo = RecruiterFeedbackRepository(db)
    feedback = await repo.get_by_match_id(match_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.patch("/feedback/{feedback_id}")
async def update_feedback(
    feedback_id: UUID,
    request: FeedbackUpdateRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    repo = RecruiterFeedbackRepository(db)
    existing = await repo.get_by_id(feedback_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Feedback not found")
        
    if request.decision is not None:
        existing.decision = request.decision
    if request.confidence is not None:
        existing.confidence = request.confidence
    if request.reason is not None:
        existing.reason = request.reason
    if request.notes is not None:
        existing.notes = request.notes
        
    existing.updated_at = datetime.utcnow()
    
    updated = await repo.update(existing)
    await db.commit()
    
    import uuid
    event = RecruiterFeedbackSubmitted(
        event_id=uuid.uuid4(),
        occurred_at=datetime.utcnow(),
        feedback_id=updated.id,
        candidate_match_id=updated.candidate_match_id,
        decision=updated.decision.value
    )
    EventBus.publish(event)
    
    return updated
