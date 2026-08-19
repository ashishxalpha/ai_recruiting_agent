from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class JobSummaryDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    # Aggregated Candidate Counts
    candidate_count: int = 0
    shortlisted_count: int = 0
    interview_count: int = 0
    hired_count: int = 0

class JobDetailsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    hiring_manager: Optional[str] = None
    status: str
    description: str
    skills_required: List[str] = []
    experience_required: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class JobCandidateMatchDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    candidate_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    semantic_score: float
    skills_score: float
    experience_score: float
    education_score: float
    quality_score: float
    final_score: float
    strengths: List[str] = []
    gaps: List[str] = []
    recommendations: List[str] = []
    created_at: datetime

class JobWorkflowDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    workflow_name: str
    workflow_version: str
    status: str
    current_node: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    candidate_id: Optional[UUID] = None
    last_error: Optional[str] = None

class JobAnalyticsDTO(BaseModel):
    total_candidates: int = 0
    average_match_score: float = 0.0
    candidates_by_status: dict[str, int] = {}
    top_skills_matched: list[str] = []

class JobFeedbackDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    candidate_id: UUID
    candidate_name: Optional[str] = None
    decision: str
    confidence: float
    reason: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

class JobHistoryDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    # Could include search parameters if added to SearchSessionModel in the future

class JobDocumentDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    file_path: str
    file_type: str
    original_name: str
    created_at: datetime
