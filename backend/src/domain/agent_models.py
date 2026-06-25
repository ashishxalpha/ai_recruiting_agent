from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class AgentLifecycle(str, Enum):
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    STOPPED = "STOPPED"
    TERMINATED = "TERMINATED"

class ExecutionMode(str, Enum):
    NORMAL = "NORMAL"
    DRY_RUN = "DRY_RUN"
    SIMULATION = "SIMULATION"
    REPLAY = "REPLAY"

class AgentCapability(BaseModel):
    required_tools: List[str] = Field(default_factory=list)
    required_memories: List[str] = Field(default_factory=list)
    required_permissions: List[str] = Field(default_factory=list)

class AgentTemplate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    default_capabilities: AgentCapability
    decision_tree: Dict[str, Any] = Field(default_factory=dict)

class AgentMemoryScope(BaseModel):
    allowed_namespaces: List[str] = Field(default_factory=list)
    max_retrieval_depth: int = 5

class Agent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    template_id: UUID
    execution_mode: ExecutionMode = ExecutionMode.NORMAL
    memory_scope: AgentMemoryScope = Field(default_factory=AgentMemoryScope)

class AgentContext(BaseModel):
    workflow_context: Dict[str, Any] = Field(default_factory=dict)
    memory_context: Dict[str, Any] = Field(default_factory=dict)
    tool_execution_context: Dict[str, Any] = Field(default_factory=dict)
    user_context: Dict[str, Any] = Field(default_factory=dict)
    system_context: Dict[str, Any] = Field(default_factory=dict)
    execution_budget: Dict[str, Any] = Field(default_factory=dict)
    conversation_state: Dict[str, Any] = Field(default_factory=dict)

class AgentObservation(BaseModel):
    event_type: str
    payload: Dict[str, Any]

class AgentThought(BaseModel):
    reasoning: str
    confidence: float

class AgentAction(BaseModel):
    action_type: str
    parameters: Dict[str, Any]

class AgentReflection(BaseModel):
    summary: str
    success_rating: float
    learnings: List[str]

class ReasoningTrace(BaseModel):
    iteration: int
    observation: AgentObservation
    thought: AgentThought
    decision: Dict[str, Any]
    action: AgentAction
    result: Dict[str, Any]
    reflection: AgentReflection
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SessionSnapshot(BaseModel):
    snapshot_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    iteration: int
    state: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AgentSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    agent_id: UUID
    workflow_id: UUID
    status: AgentLifecycle = AgentLifecycle.CREATED
    execution_history: List[ReasoningTrace] = Field(default_factory=list)
    memory_used: float = 0.0
    tools_used: List[str] = Field(default_factory=list)
    duration: float = 0.0
    cost: float = 0.0

class AgentGoal(BaseModel):
    description: str
    success_criteria: List[str]

class AgentPlan(BaseModel):
    steps: List[str]
    current_step: int = 0

class AgentExecution(BaseModel):
    execution_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    status: str
