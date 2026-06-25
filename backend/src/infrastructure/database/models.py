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

class SoftDeleteMixin:
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

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
