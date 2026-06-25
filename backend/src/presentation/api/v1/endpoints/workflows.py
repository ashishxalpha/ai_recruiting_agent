from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict
from uuid import UUID
import uuid
from pydantic import BaseModel

from src.presentation.api.dependencies import get_db

router = APIRouter()

class WorkflowStartRequest(BaseModel):
    document_id: UUID
    job_id: UUID

@router.post("")
async def start_workflow(
    request: WorkflowStartRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Start a new LangGraph workflow."""
    workflow_id = uuid.uuid4()
    # In a real setup, we would inject the WorkflowEngine from the DI container.
    # For now, we return the generated ID.
    return {
        "workflow_id": workflow_id,
        "status": "STARTED"
    }

@router.get("/{workflow_id}")
async def get_workflow_state(
    workflow_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get the current state of a workflow."""
    return {
        "workflow_id": workflow_id,
        "status": "RUNNING",
        "current_node": "ProfileEvaluationNode",
        "state_snapshot": {}
    }

@router.post("/{workflow_id}/resume")
async def resume_workflow(
    workflow_id: UUID,
    request: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Resume a paused workflow (e.g., after human approval)."""
    # In a real setup, we would inject WorkflowEngine and call engine.resume(workflow_id, request)
    # The `request` dict contains the human_feedback (e.g. {"action": "APPROVE"})
    import datetime
    from src.infrastructure.events.event_bus import EventBus
    from src.domain.workflow_events import WorkflowResumed
    
    EventBus.publish(WorkflowResumed(
        event_id=uuid.uuid4(),
        occurred_at=datetime.datetime.utcnow(),
        workflow_id=workflow_id,
        resumed_at=datetime.datetime.utcnow(),
        resumed_by="recruiter_1" # Hardcoded for MVP
    ))
    
    return {"status": "RESUMED"}

@router.post("/{workflow_id}/cancel")
async def cancel_workflow(
    workflow_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Cancel a running or paused workflow."""
    return {"status": "CANCELLED"}

@router.get("/{workflow_id}/history")
async def get_workflow_history(
    workflow_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get execution history (checkpoints) for a workflow."""
    return []

@router.get("/{workflow_id}/graph")
async def get_workflow_graph(
    workflow_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get graph metadata and progress for frontend visualization."""
    return {
        "workflow_version": "1.0.0",
        "graph_version": "1.0.0",
        "nodes": ["UploadValidationNode", "DocumentParsingNode", "AIExtractionNode", "CandidateValidationNode", "ProfileEvaluationNode"],
        "completed_nodes": ["UploadValidationNode", "DocumentParsingNode", "AIExtractionNode"],
        "current_node": "CandidateValidationNode"
    }
