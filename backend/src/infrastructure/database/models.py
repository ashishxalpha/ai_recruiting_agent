import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum, Float, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base
from src.domain.enums import CandidateStatus, JobStatus

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

class SoftDeleteMixin:
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

class CandidateModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "candidates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status: Mapped[CandidateStatus] = mapped_column(SQLEnum(CandidateStatus), default=CandidateStatus.NEW)
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    summary: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    documents: Mapped[List["CandidateDocumentModel"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    skills: Mapped[List["CandidateSkillModel"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    education: Mapped[List["CandidateEducationModel"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    experience: Mapped[List["CandidateExperienceModel"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")
    projects: Mapped[List["CandidateProjectModel"]] = relationship(back_populates="candidate", cascade="all, delete-orphan")

class CandidateDocumentModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "candidate_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True, nullable=True)
    file_path: Mapped[str] = mapped_column(String(512))
    file_type: Mapped[str] = mapped_column(String(50))
    original_name: Mapped[str] = mapped_column(String(512))
    storage_key: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text)
    extracted_text: Mapped[Optional[str]] = mapped_column(Text)

    candidate: Mapped[Optional["CandidateModel"]] = relationship(back_populates="documents")
    ai_extractions: Mapped[List["AIExtractionModel"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    ingestion_requests: Mapped[List["ResumeIngestionRequestModel"]] = relationship(back_populates="document", cascade="all, delete-orphan")

class ResumeIngestionRequestModel(Base, TimestampMixin):
    __tablename__ = "resume_ingestion_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_documents.id", ondelete="CASCADE"), index=True)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("background_jobs.id", ondelete="SET NULL"), index=True, nullable=True)
    status: Mapped[JobStatus] = mapped_column(SQLEnum(JobStatus), default=JobStatus.PENDING, index=True)

    document: Mapped["CandidateDocumentModel"] = relationship(back_populates="ingestion_requests")
    job: Mapped[Optional["BackgroundJobModel"]] = relationship()

class CandidateSkillModel(Base):
    __tablename__ = "candidate_skills"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    proficiency: Mapped[Optional[str]] = mapped_column(String(50))

    candidate: Mapped["CandidateModel"] = relationship(back_populates="skills")

class CandidateEducationModel(Base):
    __tablename__ = "candidate_education"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    institution: Mapped[str] = mapped_column(String(255))
    degree: Mapped[Optional[str]] = mapped_column(String(255))
    field_of_study: Mapped[Optional[str]] = mapped_column(String(255))
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    description: Mapped[Optional[str]] = mapped_column(Text)

    candidate: Mapped["CandidateModel"] = relationship(back_populates="education")

class CandidateExperienceModel(Base):
    __tablename__ = "candidate_experience"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    company: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    description: Mapped[Optional[str]] = mapped_column(Text)

    candidate: Mapped["CandidateModel"] = relationship(back_populates="experience")

class CandidateProjectModel(Base):
    __tablename__ = "candidate_projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(String(512))

    candidate: Mapped["CandidateModel"] = relationship(back_populates="projects")

class AIExtractionModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "ai_extractions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_documents.id", ondelete="CASCADE"), index=True)
    provider: Mapped[str] = mapped_column(String(100))
    model_name: Mapped[str] = mapped_column(String(100))
    prompt_version: Mapped[str] = mapped_column(String(50))
    schema_version: Mapped[str] = mapped_column(String(50))
    raw_ai_response: Mapped[Dict[str, Any]] = mapped_column(JSON)
    normalized_response: Mapped[Dict[str, Any]] = mapped_column(JSON)
    overall_confidence: Mapped[Optional[float]] = mapped_column(Float)
    contact_confidence: Mapped[Optional[float]] = mapped_column(Float)
    education_confidence: Mapped[Optional[float]] = mapped_column(Float)
    experience_confidence: Mapped[Optional[float]] = mapped_column(Float)
    skills_confidence: Mapped[Optional[float]] = mapped_column(Float)
    input_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    output_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    total_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer)

    document: Mapped["CandidateDocumentModel"] = relationship(back_populates="ai_extractions")

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[str] = mapped_column(String(100), index=True)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    action: Mapped[str] = mapped_column(String(50))
    changes: Mapped[Dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class BackgroundJobModel(Base, TimestampMixin):
    __tablename__ = "background_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type: Mapped[str] = mapped_column(String(100), index=True)
    correlation_id: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[JobStatus] = mapped_column(SQLEnum(JobStatus), default=JobStatus.PENDING, index=True)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

from pgvector.sqlalchemy import Vector
from sqlalchemy import Index

class JobRequirementModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "job_requirements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    skills_required: Mapped[List[str]] = mapped_column(JSON)
    experience_required: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT")
    
    # Feature 3: Jobs Workspace Fields
    department: Mapped[Optional[str]] = mapped_column(String(255))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    employment_type: Mapped[Optional[str]] = mapped_column(String(100))
    hiring_manager: Mapped[Optional[str]] = mapped_column(String(255))


class CandidateEmbeddingModel(Base):
    __tablename__ = "candidate_embeddings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    embedding_type: Mapped[str] = mapped_column(String(50), index=True)
    embedding_model: Mapped[str] = mapped_column(String(100))
    embedding_version: Mapped[str] = mapped_column(String(50))
    source_hash: Mapped[str] = mapped_column(String(255))
    vector_data = mapped_column(Vector(1536))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate: Mapped["CandidateModel"] = relationship()

class JobRequirementEmbeddingModel(Base):
    __tablename__ = "job_requirement_embeddings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_requirement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_requirements.id", ondelete="CASCADE"), index=True)
    embedding_type: Mapped[str] = mapped_column(String(50), index=True)
    embedding_model: Mapped[str] = mapped_column(String(100))
    embedding_version: Mapped[str] = mapped_column(String(50))
    source_hash: Mapped[str] = mapped_column(String(255))
    vector_data = mapped_column(Vector(1536))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    job_requirement: Mapped["JobRequirementModel"] = relationship()

# HNSW indices for fast vector search
Index('idx_candidate_embeddings_vector', CandidateEmbeddingModel.vector_data, postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'vector_data': 'vector_cosine_ops'})
Index('idx_job_requirement_embeddings_vector', JobRequirementEmbeddingModel.vector_data, postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'vector_data': 'vector_cosine_ops'})

class SearchSessionModel(Base, TimestampMixin):
    __tablename__ = "search_sessions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_requirement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_requirements.id", ondelete="CASCADE"), index=True)

class CandidateMatchModel(Base, TimestampMixin):
    __tablename__ = "candidate_matches"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("search_sessions.id", ondelete="CASCADE"), index=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    semantic_score: Mapped[float] = mapped_column(Float)
    skills_score: Mapped[float] = mapped_column(Float)
    experience_score: Mapped[float] = mapped_column(Float)
    education_score: Mapped[float] = mapped_column(Float)
    quality_score: Mapped[float] = mapped_column(Float)
    final_score: Mapped[float] = mapped_column(Float, index=True)

class MatchExplanationModel(Base, TimestampMixin):
    __tablename__ = "match_explanations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_matches.id", ondelete="CASCADE"), unique=True)
    explanation_version: Mapped[str] = mapped_column(String(50))
    strengths: Mapped[List[str]] = mapped_column(JSON)
    gaps: Mapped[List[str]] = mapped_column(JSON)
    recommendations: Mapped[List[str]] = mapped_column(JSON)

class RecruiterFeedbackModel(Base, TimestampMixin):
    __tablename__ = "recruiter_feedback"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_matches.id", ondelete="CASCADE"), index=True)
    decision: Mapped[str] = mapped_column(String(50))
    confidence: Mapped[float] = mapped_column(Float)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)

class GroundTruthEventModel(Base, TimestampMixin):
    __tablename__ = "ground_truth_events"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    job_requirement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_requirements.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(50))
    ai_score: Mapped[float] = mapped_column(Float)
    recruiter_decision: Mapped[Optional[str]] = mapped_column(String(50))


# ==========================================
# PHASE 1: Data Layer Completion Models
# ==========================================

class MemoryModel(Base, TimestampMixin, SoftDeleteMixin):
    """Metadata repository for memory entities with optimistic locking."""
    __tablename__ = "memories"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    namespace: Mapped[str] = mapped_column(String(50), index=True)
    importance: Mapped[float] = mapped_column(Float, default=0.5)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    access_count: Mapped[int] = mapped_column(Integer, default=0)
    decay_score: Mapped[float] = mapped_column(Float, default=0.0)
    retention_policy: Mapped[str] = mapped_column(String(50))
    external_reference: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    
    # Source Info
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    source_type: Mapped[str] = mapped_column(String(50))
    created_by: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Memory payload (depending on Semantic, Episodic, Procedural)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSONB)

    # Optimistic Concurrency Control
    version: Mapped[int] = mapped_column(Integer, default=1)
    
    __mapper_args__ = {
        "version_id_col": version
    }

class MemoryVectorModel(Base):
    """Independent vector repository linked to memory metadata."""
    __tablename__ = "memory_vectors"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), index=True)
    
    embedding_model: Mapped[str] = mapped_column(String(100))
    embedding_dimension: Mapped[int] = mapped_column(Integer)
    embedding_version: Mapped[str] = mapped_column(String(50))
    content_hash: Mapped[str] = mapped_column(String(255))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    vector_data = mapped_column(Vector(1536))

Index('idx_memory_vectors_data', MemoryVectorModel.vector_data, postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'vector_data': 'vector_cosine_ops'})

class MemoryEdgeModel(Base, TimestampMixin):
    """Knowledge graph foundations linking memories."""
    __tablename__ = "memory_edges"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), index=True)
    target_node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), index=True)
    relationship_type: Mapped[str] = mapped_column(String(100), index=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    provenance: Mapped[Optional[str]] = mapped_column(String(255))

class WorkingMemoryModel(Base, TimestampMixin):
    """Volatile working memory for agent sessions with expiration."""
    __tablename__ = "working_memory"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, unique=True)
    volatile_state: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), index=True)

class CheckpointModel(Base):
    """LangGraph Checkpoint Persistence."""
    __tablename__ = "checkpoints"
    thread_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    checkpoint_ns: Mapped[str] = mapped_column(String(255), primary_key=True, default="")
    checkpoint_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    parent_checkpoint_id: Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[Optional[str]] = mapped_column(String(50))
    checkpoint: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    metadata_: Mapped[Dict[str, Any]] = mapped_column("metadata", JSONB) # 'metadata' is reserved in SQLAlchemy

class CheckpointWriteModel(Base):
    """LangGraph Checkpoint Writes Persistence."""
    __tablename__ = "checkpoint_writes"
    thread_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    checkpoint_ns: Mapped[str] = mapped_column(String(255), primary_key=True, default="")
    checkpoint_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    task_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    idx: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel: Mapped[str] = mapped_column(String(255))
    type: Mapped[Optional[str]] = mapped_column(String(50))
    value: Mapped[Dict[str, Any]] = mapped_column(JSONB)

class WorkflowExecutionModel(Base):
    """Operational history of a workflow execution."""
    __tablename__ = "workflow_executions"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_name: Mapped[str] = mapped_column(String(100), index=True)
    workflow_version: Mapped[str] = mapped_column(String(50))
    thread_id: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(50), index=True)  # RUNNING, PAUSED, COMPLETED, FAILED, CANCELLED
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    current_node: Mapped[Optional[str]] = mapped_column(String(100))
    current_checkpoint_id: Mapped[Optional[str]] = mapped_column(String(255))
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[Optional[str]] = mapped_column(Text)

class ToolExecutionModel(Base):
    __tablename__ = "tool_executions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), index=True)
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), index=True)
    coordination_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    execution_budget_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    trace_id: Mapped[Optional[str]] = mapped_column(String(255), index=True)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(255))
    
    provider: Mapped[str] = mapped_column(String(255))
    tool: Mapped[str] = mapped_column(String(255))
    operation: Mapped[str] = mapped_column(String(255))
    
    status: Mapped[str] = mapped_column(String(50))
    latency_ms: Mapped[float] = mapped_column(Float)
    tokens: Mapped[Optional[int]] = mapped_column(Integer)
    cost: Mapped[Optional[float]] = mapped_column(Float)
    
    artifacts: Mapped[Optional[dict]] = mapped_column(JSONB)
    error_details: Mapped[Optional[str]] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

from sqlalchemy import Boolean
from src.domain.auth.enums import Role

class UserModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(SQLEnum(Role), default=Role.VIEWER)
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    sessions: Mapped[List["UserSessionModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reset_tokens: Mapped[List["PasswordResetTokenModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class UserSessionModel(Base, TimestampMixin):
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    refresh_token_hash: Mapped[str] = mapped_column(String(512))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(512))
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["UserModel"] = relationship(back_populates="sessions")

class PasswordResetTokenModel(Base, TimestampMixin):
    __tablename__ = "password_reset_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(512))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["UserModel"] = relationship(back_populates="reset_tokens")
