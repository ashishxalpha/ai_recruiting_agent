from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from src.domain.organization_models import OrganizationGoal, AgentSkill

class BaseOrganizationEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    organization_id: UUID

class GoalStarted(BaseOrganizationEvent):
    goal: OrganizationGoal

class GoalCompleted(BaseOrganizationEvent):
    goal_id: UUID

class SkillExecutionStarted(BaseOrganizationEvent):
    skill: AgentSkill

class SkillExecutionCompleted(BaseOrganizationEvent):
    skill_id: UUID
    success: bool

class LearningLoopTriggered(BaseOrganizationEvent):
    goal_id: UUID
