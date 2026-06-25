import uuid
from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.application.workflows.interfaces import WorkflowEngine, WorkflowDefinition, CheckpointStore
from src.application.workflows.state import RecruitingWorkflowState
from src.domain.enums import WorkflowStatus
from src.infrastructure.events.event_bus import EventBus
from src.domain.workflow_events import WorkflowStarted

class LangGraphWorkflowEngine(WorkflowEngine):
    """
    Implementation of WorkflowEngine that delegates to LangGraph.
    """
    def __init__(self, checkpointer: CheckpointStore, definitions: Dict[str, WorkflowDefinition]):
        self.checkpointer = checkpointer
        self.definitions = definitions
        self._compiled_graphs = {}

    def _get_or_compile(self, definition_name: str):
        if definition_name not in self._compiled_graphs:
            definition = self.definitions[definition_name]
            # Assumes checkpointer is a BaseCheckpointSaver subclass
            self._compiled_graphs[definition_name] = definition.compile(checkpointer=self.checkpointer)
        return self._compiled_graphs[definition_name]

    async def execute(self, definition_name: str, state: RecruitingWorkflowState, config: Dict[str, Any] = None) -> RecruitingWorkflowState:
        graph = self._get_or_compile(definition_name)
        
        definition = self.definitions[definition_name]
        
        # Build runnable config
        run_config = {
            "configurable": {
                "thread_id": state.get("workflow_id", str(uuid.uuid4()))
            },
            "metadata": {
                "workflow_id": state.get("workflow_id"),
                "candidate_id": state.get("candidate_id"),
                "job_id": state.get("job_id"),
                "workflow_version": definition.version,
                "graph_version": definition.version,
                "prompt_version": config.get("prompt_version", "latest") if config else "latest",
                "embedding_model": config.get("embedding_model", "latest") if config else "latest"
            }
        }
        if config:
            run_config.update(config)
            
        EventBus.publish(WorkflowStarted(
            event_id=uuid.uuid4(),
            occurred_at=__import__("datetime").datetime.utcnow(),
            workflow_id=uuid.UUID(state["workflow_id"]),
            candidate_document_id=uuid.UUID(state["candidate_document_id"]),
            graph_version=definition.version
        ))

        # We execute using ainvoke
        final_state = await graph.ainvoke(state, config=run_config)
        return final_state

    async def resume(self, workflow_id: uuid.UUID, user_input: Any = None) -> RecruitingWorkflowState:
        # Implementation would reload from checkpointer using thread_id=workflow_id
        # and re-invoke graph with new state/input.
        pass

    async def cancel(self, workflow_id: uuid.UUID) -> None:
        pass

    async def get_state(self, workflow_id: uuid.UUID) -> RecruitingWorkflowState:
        # Implementation fetches from checkpointer
        pass

    async def get_history(self, workflow_id: uuid.UUID) -> List[RecruitingWorkflowState]:
        # Implementation lists from checkpointer
        return []
