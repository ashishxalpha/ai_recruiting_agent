from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from src.domain.events import DomainEvent

class WorkflowStarted(DomainEvent):
    workflow_id: UUID
    candidate_document_id: UUID
    graph_version: str

class WorkflowNodeStarted(DomainEvent):
    workflow_id: UUID
    node_name: str
    started_at: datetime

class WorkflowNodeCompleted(DomainEvent):
    workflow_id: UUID
    node_name: str
    completed_at: datetime
    execution_time_ms: float

class WorkflowNodeFailed(DomainEvent):
    workflow_id: UUID
    node_name: str
    error: str
    failed_at: datetime

class WorkflowPaused(DomainEvent):
    workflow_id: UUID
    node_name: str
    interrupt_reason: str
    paused_at: datetime

class WorkflowResumed(DomainEvent):
    workflow_id: UUID
    resumed_at: datetime
    resumed_by: Optional[str] = None

class WorkflowCheckpointSaved(DomainEvent):
    workflow_id: UUID
    node_name: str
    checkpoint_id: str

class WorkflowCompleted(DomainEvent):
    workflow_id: UUID
    completed_at: datetime

class WorkflowCancelled(DomainEvent):
    workflow_id: UUID
    cancelled_at: datetime

class WorkflowFailed(DomainEvent):
    workflow_id: UUID
    failed_at: datetime
    error: str
