from pydantic import BaseModel, Field
from typing import Optional, Any, Generic, TypeVar, List, Dict
from datetime import datetime
from uuid import UUID

T = TypeVar("T")

class WorkflowResponseDTO(BaseModel, Generic[T]):
    """Standard envelope for Workflow Platform API responses."""
    status: str  # "available", "not_available", "loading", "error", "no_execution_history"
    reason: Optional[str] = None
    data: Optional[T] = None

class WorkflowSummaryDTO(BaseModel):
    id: UUID
    job_id: Optional[UUID] = None
    candidate_id: Optional[UUID] = None
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    current_node: Optional[str] = None
    workflow_version: str

# Graph Topology for React Flow
class WorkflowGraphNodeDTO(BaseModel):
    id: str
    type: str # e.g. 'customNode'
    data: Dict[str, Any]
    position: Dict[str, float]

class WorkflowGraphEdgeDTO(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = None
    type: Optional[str] = "smoothstep"

class WorkflowGraphDTO(BaseModel):
    nodes: List[WorkflowGraphNodeDTO]
    edges: List[WorkflowGraphEdgeDTO]
    current_node_id: Optional[str] = None

class WorkflowTimelineEntryDTO(BaseModel):
    event_id: UUID
    workflow_id: UUID
    timestamp: datetime
    state: str  # "Started", "Running", "Node Started", "Paused", "Human Approval", "Completed", etc.
    node_id: Optional[str] = None
    duration_ms: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkflowTimelineDTO(BaseModel):
    entries: List[WorkflowTimelineEntryDTO]

class WorkflowNodeExecutionDTO(BaseModel):
    node_id: str
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    retries: int = 0
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    tool_invocations: int = 0
    memory_retrievals: int = 0

class WorkflowNodeHistoryDTO(BaseModel):
    executions: List[WorkflowNodeExecutionDTO]

class WorkflowEventDTO(BaseModel):
    event_id: UUID
    timestamp: datetime
    category: str
    severity: str
    message: str
    node_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkflowEventListDTO(BaseModel):
    events: List[WorkflowEventDTO]

class WorkflowCheckpointDTO(BaseModel):
    checkpoint_id: str
    created_at: datetime
    resumed_at: Optional[datetime] = None
    rollback_available: bool = False
    workflow_version: str
    graph_version: str
    prompt_version: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    state_snapshot: Dict[str, Any] = Field(default_factory=dict)

class WorkflowCheckpointListDTO(BaseModel):
    checkpoints: List[WorkflowCheckpointDTO]

class WorkflowStatisticsDTO(BaseModel):
    total_duration_ms: float
    average_node_time_ms: float
    retries: int
    failures: int
    human_approvals: int
    checkpoint_count: int
    tool_calls: int
    memory_retrievals: int
