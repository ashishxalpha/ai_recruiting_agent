from typing import Any
import uuid
import datetime
from langgraph.types import interrupt
from src.application.workflows.interfaces import WorkflowNode
from src.application.workflows.state import RecruitingWorkflowState
from src.domain.enums import WorkflowStatus, InterruptReason
from src.infrastructure.events.event_bus import EventBus
from src.domain.workflow_events import WorkflowPaused

class HumanApprovalNode(WorkflowNode):
    async def execute(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
        # Determine the interrupt reason based on state context
        # (For MVP we assume LOW_CONFIDENCE if evaluating, else MANUAL_REVIEW)
        reason = InterruptReason.LOW_CONFIDENCE.value
        
        EventBus.publish(WorkflowPaused(
            event_id=uuid.uuid4(),
            occurred_at=datetime.datetime.utcnow(),
            workflow_id=uuid.UUID(state["workflow_id"]),
            node_name="HumanApprovalNode",
            interrupt_reason=reason,
            paused_at=datetime.datetime.utcnow()
        ))
        
        # Suspend graph execution here and wait for human feedback to be provided via `/resume` API
        # The `interrupt` call throws an internal exception caught by LangGraph to suspend.
        # The return value of the interrupt is the user_input provided to the resume call.
        human_feedback = interrupt({
            "status": WorkflowStatus.PAUSED.value,
            "reason": reason,
            "message": "Awaiting recruiter review of candidate profile."
        })
        
        # When resumed, the graph will continue executing from here, and `human_feedback` will be the injected value
        if isinstance(human_feedback, dict) and human_feedback.get("action") == "REJECT":
            state["workflow_status"] = WorkflowStatus.CANCELLED.value
        else:
            state["workflow_status"] = WorkflowStatus.RUNNING.value
            
        return state

    async def rollback(self, state: RecruitingWorkflowState) -> RecruitingWorkflowState:
        return state
