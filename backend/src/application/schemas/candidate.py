from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class CandidateSummaryDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    current_status: str
    profile_quality: float
    latest_workflow_status: Optional[str] = None
    latest_extraction_confidence: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class CandidateSkillDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    proficiency: Optional[str] = None

class CandidateExperienceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    company: str
    title: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class CandidateEducationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class CandidateProjectDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    description: Optional[str] = None
    url: Optional[str] = None

class CandidateProfileDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CandidateDetailsDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    profile: CandidateProfileDTO
    skills: List[CandidateSkillDTO] = []
    experience: List[CandidateExperienceDTO] = []
    education: List[CandidateEducationDTO] = []
    projects: List[CandidateProjectDTO] = []
