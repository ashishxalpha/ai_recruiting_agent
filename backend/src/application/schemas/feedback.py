from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class PendingMatchDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID  # candidate_match_id
    candidate: str
    job: str
    score: float
    status: str
    created_at: datetime

class FeedbackCreateRequest(BaseModel):
    candidate_match_id: UUID
    decision: str
    confidence: float = 1.0
    reason: Optional[str] = None
    notes: Optional[str] = None
