from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Dict, Any

class DomainEvent(BaseModel):
    event_id: UUID
    occurred_at: datetime

class CandidateMatched(DomainEvent):
    search_session_id: UUID
    job_requirement_id: UUID
    candidate_match_ids: list[UUID]

class RecruiterFeedbackSubmitted(DomainEvent):
    feedback_id: UUID
    candidate_match_id: UUID
    decision: str

class GroundTruthRecorded(DomainEvent):
    event_id: UUID
    candidate_id: UUID
    job_requirement_id: UUID
    event_type: str
