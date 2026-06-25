from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from src.domain.enums import CandidateStatus, JobStatus, JobRequirementStatus

class CurrentUser(BaseModel):
    id: UUID
    email: str
    roles: List[str] = Field(default_factory=list)

class AuthContext(BaseModel):
    user: Optional[CurrentUser] = None
    is_authenticated: bool = False

class AuditLog(BaseModel):
    id: UUID
    entity_type: str
    entity_id: UUID
    action: str
    changes: Dict[str, Any]
    created_at: datetime

class CandidateSkill(BaseModel):
    id: UUID
    candidate_id: UUID
    name: str
    proficiency: Optional[str] = None

class CandidateEducation(BaseModel):
    id: UUID
    candidate_id: UUID
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class CandidateExperience(BaseModel):
    id: UUID
    candidate_id: UUID
    company: str
    title: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class CandidateProject(BaseModel):
    id: UUID
    candidate_id: UUID
    name: str
    description: Optional[str] = None
    url: Optional[str] = None

class AIExtraction(BaseModel):
    id: UUID
    document_id: UUID
    provider: str
    model_name: str
    prompt_version: str
    schema_version: str
    raw_ai_response: Dict[str, Any]
    normalized_response: Dict[str, Any]
    overall_confidence: Optional[float] = None
    contact_confidence: Optional[float] = None
    education_confidence: Optional[float] = None
    experience_confidence: Optional[float] = None
    skills_confidence: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    processing_time_ms: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class CandidateDocument(BaseModel):
    id: UUID
    candidate_id: Optional[UUID] = None  # Optional until candidate is fully extracted
    file_path: str
    file_type: str
    original_name: str
    storage_key: str
    raw_text: Optional[str] = None
    extracted_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class ResumeIngestionRequest(BaseModel):
    id: UUID
    document_id: UUID
    job_id: Optional[UUID] = None
    status: JobStatus = JobStatus.PENDING
    created_at: datetime
    updated_at: datetime

class Candidate(BaseModel):
    id: UUID
    status: CandidateStatus = CandidateStatus.NEW
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    # Relations
    documents: List[CandidateDocument] = Field(default_factory=list)
    skills: List[CandidateSkill] = Field(default_factory=list)
    education: List[CandidateEducation] = Field(default_factory=list)
    experience: List[CandidateExperience] = Field(default_factory=list)
    projects: List[CandidateProject] = Field(default_factory=list)

class BackgroundJob(BaseModel):
    id: UUID
    job_type: str
    correlation_id: str
    status: JobStatus = JobStatus.PENDING
    payload: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class JobRequirement(BaseModel):
    id: UUID
    title: str
    description: str
    skills_required: List[str] = Field(default_factory=list)
    experience_required: Optional[str] = None
    status: JobRequirementStatus = JobRequirementStatus.DRAFT
    created_at: datetime
    updated_at: datetime

class CandidateEmbedding(BaseModel):
    id: UUID
    candidate_id: UUID
    embedding_type: str
    embedding_model: str
    embedding_version: str
    source_hash: str
    vector_data: List[float]
    generated_at: datetime

class JobRequirementEmbedding(BaseModel):
    id: UUID
    job_requirement_id: UUID
    embedding_type: str
    embedding_model: str
    embedding_version: str
    source_hash: str
    vector_data: List[float]
    generated_at: datetime

from src.domain.enums import RecruiterDecision, GroundTruthEventType

class SearchSession(BaseModel):
    id: UUID
    job_requirement_id: UUID
    created_at: datetime

class CandidateMatch(BaseModel):
    id: UUID
    search_session_id: UUID
    candidate_id: UUID
    semantic_score: float
    skills_score: float
    experience_score: float
    education_score: float
    quality_score: float
    final_score: float
    created_at: datetime
    updated_at: datetime

class MatchExplanation(BaseModel):
    id: UUID
    candidate_match_id: UUID
    explanation_version: str
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    created_at: datetime

class RecruiterFeedback(BaseModel):
    id: UUID
    candidate_match_id: UUID
    decision: RecruiterDecision
    confidence: float
    reason: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class GroundTruthEvent(BaseModel):
    id: UUID
    candidate_id: UUID
    job_requirement_id: UUID
    event_type: GroundTruthEventType
    ai_score: float
    recruiter_decision: Optional[str] = None
    created_at: datetime

class MatchingAnalytics(BaseModel):
    total_matches: int
    approved: int
    rejected: int
    shortlisted: int
    interviews: int

class CandidateMatchResult(BaseModel):
    candidate_id: UUID
    job_requirement_id: UUID
    search_session_id: Optional[UUID] = None
    semantic_score: float
    skills_score: float
    experience_score: float
    education_score: float
    final_score: float
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
