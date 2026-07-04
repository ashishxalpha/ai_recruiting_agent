import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from langgraph.errors import NodeInterrupt, GraphInterrupt

from src.application.workflows.interfaces import (
    WorkflowEngine, WorkflowDefinitionRegistry, CheckpointStore,
    RecruitingWorkflowState
)
from src.infrastructure.database.models import WorkflowExecutionModel
from src.infrastructure.events.event_bus import EventBus
from src.domain.workflow_events import WorkflowStarted

logger = logging.getLogger(__name__)

class LangGraphWorkflowEngine(WorkflowEngine):
    def __init__(self, registry: WorkflowDefinitionRegistry, checkpointer: CheckpointStore, db_session: AsyncSession):
        self.registry = registry
        self.checkpointer = checkpointer
        self.db = db_session
        
    async def execute(self, definition_name: str, state: RecruitingWorkflowState, config: Dict[str, Any] = None, version: Optional[str] = None) -> RecruitingWorkflowState:
        definition = self.registry.get(definition_name, version)
        
        thread_id = state.get("workflow_id", str(uuid.uuid4()))
        execution_id = uuid.uuid4()
        
        execution = WorkflowExecutionModel(
            id=execution_id,
            workflow_name=definition.name,
            workflow_version=definition.version,
            thread_id=thread_id,
            status="RUNNING"
        )
        self.db.add(execution)
        await self.db.commit()
        
        graph = definition.compile(checkpointer=self.checkpointer)
        
        thread_config = {
            "configurable": {"thread_id": thread_id},
            "metadata": {
                "workflow_id": state.get("workflow_id"),
                "candidate_id": state.get("candidate_id"),
                "job_id": state.get("job_id"),
                "workflow_name": definition.name,
                "workflow_version": definition.version,
                "graph_version": definition.version,
                "execution_id": str(execution_id),
                "prompt_version": config.get("prompt_version", "latest") if config else "latest",
                "embedding_model": config.get("embedding_model", "latest") if config else "latest"
            }
        }
        if config:
            thread_config["configurable"].update(config)
            
        if "workflow_id" in state:
            EventBus.publish(WorkflowStarted(
                event_id=uuid.uuid4(),
                occurred_at=datetime.utcnow(),
                workflow_id=uuid.UUID(state["workflow_id"]),
                candidate_document_id=uuid.UUID(state.get("candidate_document_id")) if state.get("candidate_document_id") else None,
                graph_version=definition.version
            ))
            
        return await self._run_graph(graph, execution, state, thread_config)
        
    async def resume(self, workflow_id: uuid.UUID, user_input: Any = None) -> RecruitingWorkflowState:
        result = await self.db.execute(
            select(WorkflowExecutionModel).where(WorkflowExecutionModel.id == workflow_id)
        )
        execution = result.scalar_one_or_none()
        if not execution:
            raise ValueError(f"Execution {workflow_id} not found.")
            
        if execution.status != "PAUSED":
            raise ValueError(f"Execution {workflow_id} is not paused (status: {execution.status}).")
            
        definition = self.registry.get(execution.workflow_name, execution.workflow_version)
        graph = definition.compile(checkpointer=self.checkpointer)
        
        thread_config = {
            "configurable": {"thread_id": execution.thread_id},
            "metadata": {
                "workflow_name": definition.name,
                "workflow_version": definition.version,
                "graph_version": definition.version,
                "execution_id": str(execution.id)
            }
        }
        
        from langgraph.types import Command
        
        execution.status = "RUNNING"
        await self.db.commit()
        
        if user_input is not None:
            # We resume by invoking the graph with a Command containing the resume value
            return await self._run_graph(graph, execution, Command(resume=user_input), thread_config)
        else:
            return await self._run_graph(graph, execution, None, thread_config)

    async def _run_graph(self, graph, execution, state, thread_config):
        try:
            # If state is None, we are resuming and don't pass initial state
            final_state = await graph.ainvoke(state, thread_config)
            
            # Check if it finished or paused
            graph_state = await graph.aget_state(thread_config)
            
            if len(graph_state.next) > 0:
                execution.status = "PAUSED"
                execution.current_node = graph_state.next[0]
            else:
                execution.status = "COMPLETED"
                execution.completed_at = datetime.utcnow()
                
            await self.db.commit()
            return final_state
        except (NodeInterrupt, GraphInterrupt) as e:
            execution.status = "PAUSED"
            # Get next pending node
            graph_state = await graph.aget_state(thread_config)
            execution.current_node = graph_state.next[0] if graph_state.next else "unknown"
            await self.db.commit()
            
            # Return current state up to the interrupt
            return graph_state.values
        except Exception as e:
            execution.status = "FAILED"
            execution.last_error = str(e)
            execution.completed_at = datetime.utcnow()
            await self.db.commit()
            raise

    async def cancel(self, workflow_id: uuid.UUID) -> None:
        result = await self.db.execute(
            select(WorkflowExecutionModel).where(WorkflowExecutionModel.id == workflow_id)
        )
        execution = result.scalar_one_or_none()
        if not execution:
            raise ValueError(f"Execution {workflow_id} not found.")
            
        execution.status = "CANCELLED"
        execution.completed_at = datetime.utcnow()
        await self.db.commit()

    async def get_state(self, workflow_id: uuid.UUID) -> RecruitingWorkflowState:
        result = await self.db.execute(
            select(WorkflowExecutionModel).where(WorkflowExecutionModel.id == workflow_id)
        )
        execution = result.scalar_one_or_none()
        if not execution:
            raise ValueError(f"Execution {workflow_id} not found.")
            
        definition = self.registry.get(execution.workflow_name, execution.workflow_version)
        graph = definition.compile(checkpointer=self.checkpointer)
        thread_config = {"configurable": {"thread_id": execution.thread_id}}
        
        graph_state = await graph.aget_state(thread_config)
        return graph_state.values

    async def get_history(self, workflow_id: uuid.UUID) -> List[RecruitingWorkflowState]:
        result = await self.db.execute(
            select(WorkflowExecutionModel).where(WorkflowExecutionModel.id == workflow_id)
        )
        execution = result.scalar_one_or_none()
        if not execution:
            raise ValueError(f"Execution {workflow_id} not found.")
            
        definition = self.registry.get(execution.workflow_name, execution.workflow_version)
        graph = definition.compile(checkpointer=self.checkpointer)
        thread_config = {"configurable": {"thread_id": execution.thread_id}}
        
        history = []
        async for state in graph.aget_state_history(thread_config):
            history.append(state.values)
            
        return history
