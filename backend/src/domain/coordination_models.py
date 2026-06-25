from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class CoordinationLifecycle(str, Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    DELEGATING = "DELEGATING"
    EXECUTING = "EXECUTING"
    WAITING = "WAITING"
    CONSENSUS = "CONSENSUS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class AgentAvailability(str, Enum):
    ONLINE = "ONLINE"
    BUSY = "BUSY"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"

class MessageType(str, Enum):
    COMMAND = "COMMAND"
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    EVENT = "EVENT"
    BROADCAST = "BROADCAST"

class SharedContextScope(str, Enum):
    GLOBAL = "GLOBAL"
    SESSION = "SESSION"
    TASK = "TASK"
    AGENT = "AGENT"

class CoordinationNode(str, Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"
    CLUSTER = "CLUSTER"

class Goal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    status: str = "PENDING"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GoalNode(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    goal_id: UUID
    status: str = "PENDING"
    payload: Dict[str, Any]

class GoalDependency(BaseModel):
    parent_id: UUID
    child_id: UUID

class DelegationTask(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    assigned_agent_id: Optional[UUID] = None
    goal_node_id: UUID
    status: str = "PENDING"
    payload: Dict[str, Any]

class DelegationPlan(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    goal_id: UUID
    tasks: List[DelegationTask] = Field(default_factory=list)

class SharedContextSnapshot(BaseModel):
    snapshot_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    scope: SharedContextScope
    state: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AgentContract(BaseModel):
    id: UUID
    description: str
    capabilities: List[str]
    supported_goals: List[str]
    required_memory: List[str]
    required_tools: List[str]
    cost_estimate: float
    health: str
    availability: AgentAvailability = AgentAvailability.ONLINE
    execution_modes: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    version: str

class AgentMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: MessageType
    sender_id: UUID
    recipient_id: Optional[UUID] = None
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AgentMailboxModel(BaseModel):
    agent_id: UUID
    messages: List[AgentMessage] = Field(default_factory=list)

class AgentConversation(BaseModel):
    conversation_id: UUID = Field(default_factory=uuid4)
    messages: List[AgentMessage] = Field(default_factory=list)

class AgentVote(BaseModel):
    agent_id: UUID
    decision: str
    confidence: float
    reason: str

class Consensus(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    goal_id: UUID
    votes: List[AgentVote] = Field(default_factory=list)
    resolution: str
    achieved: bool

class Conflict(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    involved_agents: List[UUID]
    status: str = "UNRESOLVED"

class CoordinationPolicy(BaseModel):
    delegation_rules: Dict[str, Any] = Field(default_factory=dict)
    approval_rules: Dict[str, Any] = Field(default_factory=dict)
    max_parallelism: int = 5
    timeout: int = 300
    cost_budgets: float = 10.0
    retry_policies: Dict[str, Any] = Field(default_factory=dict)
    conflict_strategy: str = "MAJORITY"
    human_approval_required: bool = False

class CoordinationSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    status: CoordinationLifecycle = CoordinationLifecycle.CREATED
    node: CoordinationNode = CoordinationNode.LOCAL
    policy: CoordinationPolicy = Field(default_factory=CoordinationPolicy)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    duration: float = 0.0
