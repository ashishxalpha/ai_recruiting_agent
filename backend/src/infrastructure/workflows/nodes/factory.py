from src.application.workflows.state import RecruitingWorkflowState
from src.application.workflows.interfaces import WorkflowNode

from typing import Optional
from src.application.workflows.interfaces import NodeRetryPolicy

# Factory helper for wrapping simple application services
def create_service_node(service_function, node_name: str, retry_policy: Optional[NodeRetryPolicy] = None) -> WorkflowNode:
    class ServiceNodeWrapper(WorkflowNode):
        @property
        def retry_policy(self) -> Optional[NodeRetryPolicy]:
            return retry_policy
        async def execute(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
            import uuid
            import datetime
            from src.infrastructure.events.event_bus import EventBus
            from src.domain.workflow_events import WorkflowNodeStarted, WorkflowNodeCompleted, WorkflowNodeFailed
            
            EventBus.publish(WorkflowNodeStarted(
                event_id=uuid.uuid4(),
                occurred_at=datetime.datetime.utcnow(),
                workflow_id=uuid.UUID(state["workflow_id"]),
                node_name=node_name,
                started_at=datetime.datetime.utcnow()
            ))
            
            start_time = datetime.datetime.utcnow()
            
            try:
                # Call underlying service function
                new_state = await service_function(state)
                
                execution_time = (datetime.datetime.utcnow() - start_time).total_seconds() * 1000
                EventBus.publish(WorkflowNodeCompleted(
                    event_id=uuid.uuid4(),
                    occurred_at=datetime.datetime.utcnow(),
                    workflow_id=uuid.UUID(state["workflow_id"]),
                    node_name=node_name,
                    completed_at=datetime.datetime.utcnow(),
                    execution_time_ms=execution_time
                ))
                return new_state
                
            except Exception as e:
                EventBus.publish(WorkflowNodeFailed(
                    event_id=uuid.uuid4(),
                    occurred_at=datetime.datetime.utcnow(),
                    workflow_id=uuid.UUID(state["workflow_id"]),
                    node_name=node_name,
                    error=str(e),
                    failed_at=datetime.datetime.utcnow()
                ))
                raise e

        async def rollback(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
            # Empty rollback by default
            return state

    return ServiceNodeWrapper()
