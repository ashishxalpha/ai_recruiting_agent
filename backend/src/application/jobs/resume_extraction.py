import logging
import uuid
from datetime import datetime
from typing import Dict, Any

from src.domain.entities import Candidate, CandidateSkill, CandidateEducation, CandidateExperience, CandidateProject, AIExtraction
from src.domain.enums import CandidateStatus, JobStatus
from src.domain.interfaces.repositories import (
    CandidateRepository, CandidateDocumentRepository, JobRepository, AIExtractionRepository
)
from src.domain.interfaces.providers import StorageProvider
from src.infrastructure.parsers.base import DocumentParser
from src.infrastructure.parsers.pdf import PDFParser
from src.infrastructure.parsers.docx import DOCXParser
from src.infrastructure.providers.ai.openai import AIExtractionProvider
from src.application.services.validation import CandidateProfileValidator
from src.application.services.evaluation import ProfileEvaluator
from src.domain.interfaces.dlq import FailedExtractionTrackingProvider
from src.core.prompts.registry import registry
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)
logger = logging.getLogger(__name__)

from src.domain.interfaces.embedding import EmbeddingProvider
from src.infrastructure.database.repositories.embedding_repository import CandidateEmbeddingRepository

class ResumeExtractionWorkflow:
    def __init__(
        self,
        job_repo: JobRepository,
        document_repo: CandidateDocumentRepository,
        candidate_repo: CandidateRepository,
        extraction_repo: AIExtractionRepository,
        storage_provider: StorageProvider,
        ai_provider: AIExtractionProvider,
        dlq_provider: FailedExtractionTrackingProvider,
        validator: CandidateProfileValidator,
        evaluator: ProfileEvaluator,
        embedding_provider: EmbeddingProvider = None,
        embedding_repo: CandidateEmbeddingRepository = None
    ):
        self.job_repo = job_repo
        self.document_repo = document_repo
        self.candidate_repo = candidate_repo
        self.extraction_repo = extraction_repo
        self.storage_provider = storage_provider
        self.ai_provider = ai_provider
        self.dlq_provider = dlq_provider
        self.validator = validator
        self.evaluator = evaluator
        self.embedding_provider = embedding_provider
        self.embedding_repo = embedding_repo

    async def execute(self, job_id: uuid.UUID) -> None:
        with tracer.start_as_current_span("ResumeExtractionWorkflow.execute"):
            job = await self.job_repo.get_by_id(job_id)
            if not job:
                logger.error(f"Job {job_id} not found.")
                return

            if job.status not in [JobStatus.PENDING, JobStatus.QUEUED, JobStatus.RETRYING]:
                logger.warning(f"Job {job_id} is in status {job.status}. Skipping.")
                return

            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            await self.job_repo.update(job)

            try:
                document_id_str = job.payload.get("document_id")
                if not document_id_str:
                    raise ValueError("document_id missing from job payload")
                document_id = uuid.UUID(document_id_str)

                document = await self.document_repo.get_by_id(document_id)
                if not document:
                    raise ValueError(f"Document {document_id} not found")

                # 1. Parsing
                file_bytes = await self.storage_provider.get_file(document.storage_key)
                
                parser: DocumentParser
                if document.file_type == "application/pdf":
                    parser = PDFParser()
                elif document.file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                    parser = DOCXParser()
                else:
                    raise ValueError(f"Unsupported file type: {document.file_type}")

                doc_content = parser.parse(file_bytes)
                document.raw_text = doc_content.text
                await self.document_repo.update(document)

                # 2. AI Extraction
                prompt_template = registry.get_prompt("resume_extraction", "v1")
                profile, metrics = await self.ai_provider.extract_profile(document.raw_text, prompt_template)

                # 3. Validation
                profile = self.validator.validate(profile)

                # 4. Evaluation
                eval_result = self.evaluator.evaluate(profile)

                # 5. Store Extraction Record
                extraction = AIExtraction(
                    id=uuid.uuid4(),
                    document_id=document.id,
                    provider=metrics["provider"],
                    model_name=metrics["model_name"],
                    prompt_version="v1",
                    schema_version="v1",
                    raw_ai_response=metrics["raw_response"],
                    normalized_response=profile.model_dump(),
                    overall_confidence=eval_result.confidence_score,
                    contact_confidence=eval_result.contact_confidence,
                    education_confidence=eval_result.education_confidence,
                    experience_confidence=eval_result.experience_confidence,
                    skills_confidence=eval_result.skills_confidence,
                    input_tokens=metrics["input_tokens"],
                    output_tokens=metrics["output_tokens"],
                    total_tokens=metrics["total_tokens"],
                    processing_time_ms=metrics["processing_time_ms"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                await self.extraction_repo.create(extraction)

                # 6. Candidate Generation
                candidate = Candidate(
                    id=uuid.uuid4(),
                    status=CandidateStatus.UNDER_REVIEW,
                    first_name=profile.first_name,
                    last_name=profile.last_name,
                    email=profile.email,
                    phone=profile.phone,
                    summary=profile.summary,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )

                candidate.skills = [
                    CandidateSkill(id=uuid.uuid4(), candidate_id=candidate.id, name=s.name, proficiency=s.proficiency)
                    for s in profile.skills
                ]
                candidate.education = [
                    CandidateEducation(
                        id=uuid.uuid4(), candidate_id=candidate.id, institution=e.institution,
                        degree=e.degree, field_of_study=e.field_of_study, start_date=e.start_date,
                        end_date=e.end_date, description=e.description
                    ) for e in profile.education
                ]
                candidate.experience = [
                    CandidateExperience(
                        id=uuid.uuid4(), candidate_id=candidate.id, company=e.company,
                        title=e.title, start_date=e.start_date, end_date=e.end_date, description=e.description
                    ) for e in profile.experience
                ]
                candidate.projects = [
                    CandidateProject(
                        id=uuid.uuid4(), candidate_id=candidate.id, name=p.name,
                        description=p.description, url=p.url
                    ) for p in profile.projects
                ]

                await self.candidate_repo.create(candidate)

                # Link document to candidate
                document.candidate_id = candidate.id
                await self.document_repo.update(document)

                # Generate Embeddings (Optional)
                if self.embedding_provider and self.embedding_repo:
                    import hashlib
                    from src.domain.entities import CandidateEmbedding
                    from src.domain.enums import EmbeddingType
                    
                    full_text = f"{profile.first_name} {profile.last_name}\n\n{profile.summary}\n\n"
                    full_text += "Skills:\n" + ", ".join([s.name for s in profile.skills]) + "\n\n"
                    full_text += "Experience:\n" + "\n".join([f"{e.title} at {e.company}: {e.description}" for e in profile.experience])
                    
                    source_hash = hashlib.sha256(full_text.encode()).hexdigest()
                    vector = await self.embedding_provider.generate_embedding(full_text)
                    
                    embedding = CandidateEmbedding(
                        id=uuid.uuid4(),
                        candidate_id=candidate.id,
                        embedding_type=EmbeddingType.FULL_PROFILE.value,
                        embedding_model=self.embedding_provider.model_name,
                        embedding_version=self.embedding_provider.embedding_version,
                        source_hash=source_hash,
                        vector_data=vector,
                        generated_at=datetime.utcnow()
                    )
                    await self.embedding_repo.create_batch([embedding])

                # 7. Complete Job
                job.status = JobStatus.COMPLETED
                job.completed_at = datetime.utcnow()
                job.result = {
                    "candidate_id": str(candidate.id),
                    "extraction_id": str(extraction.id),
                    "confidence": eval_result.confidence_score
                }
                await self.job_repo.update(job)
                logger.info(f"Successfully extracted profile for job {job_id}")

            except Exception as e:
                logger.exception(f"Job {job_id} failed with error: {e}")
                job.status = JobStatus.FAILED
                job.error_message = str(e)
                job.completed_at = datetime.utcnow()
                await self.job_repo.update(job)
                
                # Send to DLQ
                doc_id = locals().get("document_id")
                await self.dlq_provider.track_failure(
                    document_id=doc_id,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    payload=job.payload
                )
