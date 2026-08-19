from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict
from uuid import UUID
import uuid
from pydantic import BaseModel

from src.presentation.api.dependencies import get_db_session
from src.application.services.workflows.workflow_query_service import WorkflowQueryService
from src.application.schemas.workflow import (
    WorkflowResponseDTO,
    WorkflowSummaryDTO,
    WorkflowGraphDTO,
    WorkflowTimelineDTO,
    WorkflowNodeHistoryDTO,
    WorkflowEventListDTO,
    WorkflowCheckpointListDTO,
    WorkflowStatisticsDTO
)

router = APIRouter()

class WorkflowStartRequest(BaseModel):
    document_id: UUID
    job_id: UUID

def get_workflow_query_service(db: AsyncSession = Depends(get_db_session)) -> WorkflowQueryService:
    return WorkflowQueryService(db)

from src.application.workflows.interfaces import WorkflowEngine
from src.presentation.api.dependencies import get_workflow_engine

# --- Write Endpoints (Engine Orchestration) ---

@router.post("")
async def start_workflow(request: WorkflowStartRequest,
    engine: WorkflowEngine = Depends(get_workflow_engine),
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """Start a new LangGraph workflow."""
    state = {
        "workflow_id": str(uuid.uuid4()),
        "candidate_document_id": str(request.document_id),
        "job_id": str(request.job_id) if request.job_id else None
    }
    
    await engine.execute("resume_extraction_workflow", state)
    
    return {
        "workflow_id": state["workflow_id"],
        "status": "STARTED"
    }

@router.post("/{workflow_id}/resume")
async def resume_workflow(workflow_id: UUID,
    request: Dict[str, Any],
    engine: WorkflowEngine = Depends(get_workflow_engine),
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """Resume a paused workflow (e.g., after human approval)."""
    await engine.resume(workflow_id, request)
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.post("/{workflow_id}/cancel")
async def cancel_workflow(workflow_id: UUID,
    engine: WorkflowEngine = Depends(get_workflow_engine),
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """Cancel a running or paused workflow."""
    await engine.cancel(workflow_id)
    raise HTTPException(status_code=501, detail="feature_available: false")


# --- Read Endpoints (Workflow Platform Observability) ---

@router.get("/{workflow_id}", response_model=WorkflowResponseDTO[WorkflowSummaryDTO])
async def get_workflow_summary(
    workflow_id: UUID,
    service: WorkflowQueryService = Depends(get_workflow_query_service)
):
    """Get the current summary state of a workflow."""
    return await service.get_summary(workflow_id)

@router.get("/{workflow_id}/timeline", response_model=WorkflowResponseDTO[WorkflowTimelineDTO])
async def get_workflow_timeline(
    workflow_id: UUID,
    service: WorkflowQueryService = Depends(get_workflow_query_service)
):
    """Get lifecycle transitions (Started, Paused, Resumed, etc)."""
    return await service.get_timeline(workflow_id)

@router.get("/{workflow_id}/graph", response_model=WorkflowResponseDTO[WorkflowGraphDTO])
async def get_workflow_graph(
    workflow_id: UUID,
    service: WorkflowQueryService = Depends(get_workflow_query_service)
):
    """Get graph topology and execution status for UI rendering."""
    return await service.get_graph(workflow_id)

@router.get("/{workflow_id}/nodes", response_model=WorkflowResponseDTO[WorkflowNodeHistoryDTO])
async def get_workflow_nodes(
    workflow_id: UUID,
    service: WorkflowQueryService = Depends(get_workflow_query_service)
):
    """Get execution history and performance for individual nodes."""
    return await service.get_nodes(workflow_id)

@router.get("/{workflow_id}/events", response_model=WorkflowResponseDTO[WorkflowEventListDTO])
async def get_workflow_events(
    workflow_id: UUID,
    service: WorkflowQueryService = Depends(get_workflow_query_service)
):
    """Get EventBus history related to this workflow."""
    return await service.get_events(workflow_id)

@router.get("/{workflow_id}/checkpoints", response_model=WorkflowResponseDTO[WorkflowCheckpointListDTO])
async def get_workflow_checkpoints(
    workflow_id: UUID,
    service: WorkflowQueryService = Depends(get_workflow_query_service)
):
    """Get LangGraph persisted checkpoints."""
    return await service.get_checkpoints(workflow_id)

@router.get("/{workflow_id}/statistics", response_model=WorkflowResponseDTO[WorkflowStatisticsDTO])
async def get_workflow_statistics(
    workflow_id: UUID,
    service: WorkflowQueryService = Depends(get_workflow_query_service)
):
    """Get aggregated workflow statistics."""
    return await service.get_statistics(workflow_id)
