from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from src.domain.agent_models import AgentObservation, AgentThought, AgentReflection, AgentAction

class BaseAgentEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    agent_id: UUID
    session_id: UUID

class AgentCreated(BaseAgentEvent):
    template_id: UUID

class AgentStarted(BaseAgentEvent):
    pass

class AgentPaused(BaseAgentEvent):
    reason: str

class AgentResumed(BaseAgentEvent):
    pass

class AgentStopped(BaseAgentEvent):
    pass

class AgentFailed(BaseAgentEvent):
    error: str

class AgentObservationCreated(BaseAgentEvent):
    observation: AgentObservation

class AgentThoughtCreated(BaseAgentEvent):
    thought: AgentThought

class AgentReflectionCreated(BaseAgentEvent):
    reflection: AgentReflection

class AgentActionExecuted(BaseAgentEvent):
    action: AgentAction
    success: bool
