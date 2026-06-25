from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, Any

class BaseToolEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    provider_id: str
    tool_id: str

class ToolRegistered(BaseToolEvent):
    capabilities: list[str]

class ToolDiscovered(BaseToolEvent):
    metadata: Dict[str, Any]

class ToolExecutionStarted(BaseToolEvent):
    session_id: UUID
    execution_id: UUID

class ToolExecutionCompleted(BaseToolEvent):
    session_id: UUID
    execution_id: UUID
    success: bool
    execution_time: float
    cost: float

class ToolExecutionFailed(BaseToolEvent):
    session_id: UUID
    execution_id: UUID
    error_message: str

class ToolPermissionDenied(BaseToolEvent):
    session_id: UUID
    reason: str

class ToolHealthChanged(BaseToolEvent):
    old_status: str
    new_status: str
