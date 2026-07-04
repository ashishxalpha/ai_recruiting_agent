from __future__ import annotations
from typing import Protocol, Any, Dict, List, Optional
from uuid import UUID
from src.application.workflows.state import RecruitingWorkflowState

class NodeRetryPolicy(Protocol):
    """Defines retry behavior for a specific node."""
    max_attempts: int
    backoff_multiplier: float
    retry_on_exceptions: List[type[Exception]]

class WorkflowNode(Protocol):
    """A generic node inside a workflow definition."""
    
    @property
    def retry_policy(self) -> Optional[NodeRetryPolicy]:
        """Optionally returns a retry policy for this node."""
        return None
        
    async def execute(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
        """Executes the business logic of the node."""
        ...
        
    async def rollback(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
        """Rollback actions if execution fails downstream."""
        ...

class WorkflowDefinition(Protocol):
    """Defines the graph layout and logic for a workflow."""
    name: str
    version: str
    configuration: Dict[str, Any]
    supported_states: List[str]
    required_capabilities: List[str]
    
    def compile(self, checkpointer: CheckpointStore = None) -> Any:
        """Compiles definition into executable format (e.g. LangGraph CompiledGraph)."""
        ...

class WorkflowDefinitionRegistry(Protocol):
    """Registry for managing versioned workflow definitions."""
    def register(self, definition: WorkflowDefinition) -> None:
        ...
        
    def get(self, name: str, version: Optional[str] = None) -> WorkflowDefinition:
        ...
        
    def list(self) -> List[WorkflowDefinition]:
        ...
        
    def exists(self, name: str, version: Optional[str] = None) -> bool:
        ...
        
    def latest_version(self, name: str) -> Optional[str]:
        ...

class NodeRegistry(Protocol):
    """Responsible for resolving workflow nodes."""
    def get_node(self, node_name: str) -> WorkflowNode:
        ...
        
    def register_node(self, node_name: str, node: WorkflowNode) -> None:
        ...

class CheckpointStore(Protocol):
    """Abstract store for managing checkpoint persistence."""
    pass
    # Actual implementation methods depend on the underlying engine needs, 
    # but the application interacts with it opaquely.

class WorkflowExecutionRecord(Protocol):
    """Record of a workflow execution run."""
    id: UUID
    workflow_name: str
    workflow_version: str
    thread_id: str
    status: str
    current_node: Optional[str]
    current_checkpoint_id: Optional[str]
    retry_count: int

class WorkflowEngine(Protocol):
    """Orchestrates execution of workflows without exposing underlying engine (e.g. LangGraph)."""
    
    async def execute(self, definition_name: str, state: RecruitingWorkflowState, config: Dict[str, Any] = None, version: Optional[str] = None) -> RecruitingWorkflowState:
        """Starts or continues a workflow."""
        ...
        
    async def resume(self, workflow_id: UUID, user_input: Any = None) -> RecruitingWorkflowState:
        """Resumes a paused workflow."""
        ...
        
    async def cancel(self, workflow_id: UUID) -> None:
        """Cancels a workflow."""
        ...
        
    async def get_state(self, workflow_id: UUID) -> RecruitingWorkflowState:
        """Retrieves the current state of a workflow."""
        ...
        
    async def get_history(self, workflow_id: UUID) -> List[RecruitingWorkflowState]:
        """Retrieves the history of states for a workflow."""
        ...
