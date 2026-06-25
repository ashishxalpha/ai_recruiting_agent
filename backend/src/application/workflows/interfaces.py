from typing import Protocol, Any, Dict, List
from uuid import UUID
from src.application.workflows.state import RecruitingWorkflowState

class WorkflowNode(Protocol):
    """A generic node inside a workflow definition."""
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
    
    def compile(self, checkpointer: CheckpointStore = None) -> Any:
        """Compiles definition into executable format (e.g. LangGraph CompiledGraph)."""
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

class WorkflowEngine(Protocol):
    """Orchestrates execution of workflows without exposing underlying engine (e.g. LangGraph)."""
    
    async def execute(self, definition_name: str, state: RecruitingWorkflowState, config: Dict[str, Any] = None) -> RecruitingWorkflowState:
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
