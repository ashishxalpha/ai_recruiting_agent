from typing import TypedDict, Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from src.domain.enums import WorkflowStatus

class RecruitingWorkflowState(TypedDict, total=False):
    """
    Central state object orchestrating the recruiting pipeline.
    Must be fully serializable for checkpointing.
    """
    workflow_id: str
    candidate_document_id: str
    candidate_id: Optional[str]
    job_id: Optional[str]
    search_session_id: Optional[str]
    
    current_step: str
    workflow_status: str  # WorkflowStatus value
    
    # State accumulated across nodes
    raw_text: Optional[str]
    candidate_profile: Optional[Dict[str, Any]]
    embedding_ids: List[str]
    candidate_matches: List[Dict[str, Any]]
    evaluation_result: Optional[Dict[str, Any]]
    
    # Execution Tracking
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]
    timestamps: Dict[str, str]
