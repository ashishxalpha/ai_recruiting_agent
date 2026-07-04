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
