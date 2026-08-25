import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from pydantic import BaseModel

from src.application.workflows.interfaces import WorkflowEngine
from src.presentation.api.dependencies import get_workflow_engine
from src.observability.tracing import get_tracer

router = APIRouter(prefix="/outreach", tags=["Outreach Agent"])
tracer = get_tracer(__name__)

class OutreachStartRequest(BaseModel):
    job_id: UUID
    candidate_id: UUID

class OutreachStartResponse(BaseModel):
    workflow_id: str
    status: str
    message: str
    draft_email_content: str = None

class OutreachResumeRequest(BaseModel):
    action: str  # "APPROVED" or "REJECTED" or "EDITED"
    draft_email_content: str = None

@router.post("/start", response_model=OutreachStartResponse)
async def start_outreach_workflow(
    request: OutreachStartRequest,
    engine: WorkflowEngine = Depends(get_workflow_engine)
) -> Any:
    """Start the outreach agent workflow for a job and candidate."""
    with tracer.start_as_current_span("API.POST./api/v1/outreach/start"):
        workflow_id = str(uuid.uuid4())
        initial_state = {
            "workflow_id": workflow_id,
            "job_id": str(request.job_id),
            "candidate_id": str(request.candidate_id),
            "current_step": "START",
            "workflow_status": "RUNNING"
        }
        
        try:
            state = await engine.execute(
                definition_name="outreach_agent",
                state=initial_state
            )
            
            # The execution_id is normally available in state['metadata']['execution_id']
            # or thread_id which maps to it. Let's return thread_id for now as workflow_id
            workflow_id = state.get("workflow_id", "unknown")
            if "metadata" in state and "execution_id" in state["metadata"]:
                workflow_id = state["metadata"]["execution_id"]

            return {
                "workflow_id": workflow_id,
                "status": state.get("email_status", "UNKNOWN"),
                "message": "Outreach agent started successfully",
                "draft_email_content": state.get("draft_email_content")
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/{workflow_id}/resume")
async def resume_outreach_workflow(
    workflow_id: UUID,
    request: OutreachResumeRequest,
    engine: WorkflowEngine = Depends(get_workflow_engine)
) -> Any:
    """Resume a paused outreach workflow."""
    with tracer.start_as_current_span("API.POST./api/v1/outreach/{workflow_id}/resume"):
        user_input = {
            "status": request.action,
            "draft_email_content": request.draft_email_content
        }
        
        try:
            state = await engine.resume(workflow_id, user_input=user_input)
            
            return {
                "workflow_id": str(workflow_id),
                "status": state.get("email_status", "UNKNOWN"),
                "message": "Outreach agent resumed successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
