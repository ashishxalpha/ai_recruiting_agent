from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from src.domain.coordination_models import AgentMessage, Consensus, Conflict, Goal, DelegationPlan

class BaseCoordinationEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    session_id: UUID

class SessionStatusChanged(BaseCoordinationEvent):
    old_status: str
    new_status: str

class GoalSubmitted(BaseCoordinationEvent):
    goal: Goal

class DelegationPlanCreated(BaseCoordinationEvent):
    plan: DelegationPlan

class MessageRouted(BaseCoordinationEvent):
    message: AgentMessage

class ConsensusReached(BaseCoordinationEvent):
    consensus: Consensus

class ConflictDetected(BaseCoordinationEvent):
    conflict: Conflict

class ConflictResolved(BaseCoordinationEvent):
    conflict_id: UUID
    resolution: str
