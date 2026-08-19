from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc
from uuid import UUID
from typing import Optional, List, Dict, Any

from src.application.schemas.job import (
    JobSummaryDTO, JobDetailsDTO, JobCandidateMatchDTO,
    JobWorkflowDTO, JobAnalyticsDTO, JobFeedbackDTO,
    JobHistoryDTO, JobDocumentDTO
)
from src.application.schemas.candidate import CandidateSummaryDTO
from src.application.schemas.pagination import PaginatedResponse
from src.infrastructure.database.models import (
    JobRequirementModel,
    CandidateModel,
    CandidateDocumentModel,
    ResumeIngestionRequestModel,
    CandidateMatchModel,
    SearchSessionModel,
    MatchExplanationModel,
    WorkflowExecutionModel,
    RecruiterFeedbackModel
)

class JobQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_jobs(
        self,
        page: int,
        page_size: int,
        search: Optional[str] = None,
        status: Optional[str] = None,
        department: Optional[str] = None,
        location: Optional[str] = None,
        employment_type: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> PaginatedResponse[JobSummaryDTO]:
        
        stmt = select(JobRequirementModel)
        count_stmt = select(func.count(JobRequirementModel.id))

        # Filters
        if status:
            from src.domain.enums import JobRequirementStatus
            try:
                status_enum = JobRequirementStatus(status)
                stmt = stmt.where(JobRequirementModel.status == status_enum)
                count_stmt = count_stmt.where(JobRequirementModel.status == status_enum)
            except ValueError:
                pass
                
        if department:
            stmt = stmt.where(JobRequirementModel.department == department)
            count_stmt = count_stmt.where(JobRequirementModel.department == department)
            
        if location:
            stmt = stmt.where(JobRequirementModel.location == location)
            count_stmt = count_stmt.where(JobRequirementModel.location == location)
            
        if employment_type:
            stmt = stmt.where(JobRequirementModel.employment_type == employment_type)
            count_stmt = count_stmt.where(JobRequirementModel.employment_type == employment_type)

        if search:
            search_pattern = f"%{search}%"
            stmt = stmt.where(
                (JobRequirementModel.title.ilike(search_pattern)) |
                (JobRequirementModel.description.ilike(search_pattern))
            )
            count_stmt = count_stmt.where(
                (JobRequirementModel.title.ilike(search_pattern)) |
                (JobRequirementModel.description.ilike(search_pattern))
            )

        total = (await self.session.execute(count_stmt)).scalar() or 0
        total_pages = max(1, (total + page_size - 1) // page_size)

        # Sorting
        sort_col = getattr(JobRequirementModel, sort_by, JobRequirementModel.created_at)
        if sort_order.lower() == "desc":
            stmt = stmt.order_by(desc(sort_col))
        else:
            stmt = stmt.order_by(asc(sort_col))

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.session.execute(stmt)
        jobs = result.scalars().all()

        items = []
        for j in jobs:
            items.append(JobSummaryDTO(
                id=j.id,
                title=j.title,
                department=j.department,
                location=j.location,
                employment_type=j.employment_type,
                status=j.status,
                created_at=j.created_at,
                updated_at=j.updated_at,
                candidate_count=0, # Aggregations can be added later
                shortlisted_count=0,
                interview_count=0,
                hired_count=0
            ))

        return PaginatedResponse(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )

    async def get_job_details(self, id: UUID) -> Optional[JobDetailsDTO]:
        stmt = select(JobRequirementModel).where(JobRequirementModel.id == id)
        result = await self.session.execute(stmt)
        job = result.scalar_one_or_none()
        
        if not job:
            return None
            
        return JobDetailsDTO(
            id=job.id,
            title=job.title,
            department=job.department,
            location=job.location,
            employment_type=job.employment_type,
            hiring_manager=job.hiring_manager,
            status=job.status,
            description=job.description,
            skills_required=job.skills_required or [],
            experience_required=job.experience_required,
            created_at=job.created_at,
            updated_at=job.updated_at
        )

    async def get_job_candidates(self, job_id: UUID) -> List[CandidateSummaryDTO]:
        stmt = (
            select(CandidateModel)
            .join(CandidateDocumentModel, CandidateDocumentModel.candidate_id == CandidateModel.id)
            .join(ResumeIngestionRequestModel, ResumeIngestionRequestModel.document_id == CandidateDocumentModel.id)
            .where(ResumeIngestionRequestModel.job_id == job_id)
            .distinct()
            .order_by(desc(CandidateModel.created_at))
        )
        result = await self.session.execute(stmt)
        candidates = result.scalars().all()
        
        return [
            CandidateSummaryDTO(
                id=c.id,
                full_name=f"{c.first_name or ''} {c.last_name or ''}".strip() or "Unknown",
                email=c.email,
                phone=c.phone,
                current_status=c.status.value,
                profile_quality=0.0, # calculate or fetch from another table
                created_at=c.created_at,
                updated_at=c.updated_at
            ) for c in candidates
        ]

    async def get_job_matches(self, job_id: UUID) -> List[JobCandidateMatchDTO]:
        stmt = (
            select(CandidateMatchModel, CandidateModel, MatchExplanationModel)
            .join(SearchSessionModel, SearchSessionModel.id == CandidateMatchModel.search_session_id)
            .join(CandidateModel, CandidateModel.id == CandidateMatchModel.candidate_id)
            .outerjoin(MatchExplanationModel, MatchExplanationModel.candidate_match_id == CandidateMatchModel.id)
            .where(SearchSessionModel.job_requirement_id == job_id)
            .order_by(desc(CandidateMatchModel.final_score))
        )
        result = await self.session.execute(stmt)
        matches = result.all()
        
        dtos = []
        for match, candidate, explanation in matches:
            dtos.append(JobCandidateMatchDTO(
                id=match.id,
                candidate_id=candidate.id,
                first_name=candidate.first_name,
                last_name=candidate.last_name,
                email=candidate.email,
                semantic_score=match.semantic_score,
                skills_score=match.skills_score,
                experience_score=match.experience_score,
                education_score=match.education_score,
                quality_score=match.quality_score,
                final_score=match.final_score,
                strengths=explanation.strengths if explanation else [],
                gaps=explanation.gaps if explanation else [],
                recommendations=explanation.recommendations if explanation else [],
                created_at=match.created_at
            ))
        return dtos

    async def get_job_workflows(self, job_id: UUID) -> List[JobWorkflowDTO]:
        stmt = (
            select(WorkflowExecutionModel)
            .where(WorkflowExecutionModel.job_id == job_id)
            .order_by(desc(WorkflowExecutionModel.started_at))
        )
        result = await self.session.execute(stmt)
        executions = result.scalars().all()
        
        return [
            JobWorkflowDTO(
                id=e.id,
                workflow_name=e.workflow_name,
                workflow_version=e.workflow_version,
                status=e.status,
                current_node=e.current_node,
                started_at=e.started_at,
                completed_at=e.completed_at,
                candidate_id=e.candidate_id,
                last_error=e.last_error
            ) for e in executions
        ]

    async def get_job_analytics(self, job_id: UUID) -> JobAnalyticsDTO:
        # Get total candidates
        candidates_stmt = (
            select(func.count(func.distinct(CandidateModel.id)))
            .join(CandidateDocumentModel, CandidateDocumentModel.candidate_id == CandidateModel.id)
            .join(ResumeIngestionRequestModel, ResumeIngestionRequestModel.document_id == CandidateDocumentModel.id)
            .where(ResumeIngestionRequestModel.job_id == job_id)
        )
        total_candidates = (await self.session.execute(candidates_stmt)).scalar() or 0

        # Get average match score
        score_stmt = (
            select(func.avg(CandidateMatchModel.final_score))
            .join(SearchSessionModel, SearchSessionModel.id == CandidateMatchModel.search_session_id)
            .where(SearchSessionModel.job_requirement_id == job_id)
        )
        avg_score = (await self.session.execute(score_stmt)).scalar() or 0.0

        # Note: We can add more complex analytics here (candidates_by_status, top_skills)
        return JobAnalyticsDTO(
            total_candidates=total_candidates,
            average_match_score=float(avg_score),
            candidates_by_status={},
            top_skills_matched=[]
        )

    async def get_job_feedback(self, job_id: UUID) -> List[JobFeedbackDTO]:
        stmt = (
            select(RecruiterFeedbackModel, CandidateModel)
            .join(CandidateMatchModel, CandidateMatchModel.id == RecruiterFeedbackModel.candidate_match_id)
            .join(SearchSessionModel, SearchSessionModel.id == CandidateMatchModel.search_session_id)
            .join(CandidateModel, CandidateModel.id == CandidateMatchModel.candidate_id)
            .where(SearchSessionModel.job_requirement_id == job_id)
            .order_by(desc(RecruiterFeedbackModel.created_at))
        )
        result = await self.session.execute(stmt)
        feedback_records = result.all()
        
        return [
            JobFeedbackDTO(
                id=f.id,
                candidate_id=c.id,
                candidate_name=f"{c.first_name or ''} {c.last_name or ''}".strip() or "Unknown",
                decision=f.decision,
                confidence=f.confidence,
                reason=f.reason,
                notes=f.notes,
                created_at=f.created_at
            ) for f, c in feedback_records
        ]

    async def get_job_documents(self, job_id: UUID) -> List[JobDocumentDTO]:
        # Currently no Job Document Model is directly mapped to JobRequirement for attachments.
        return []

    async def get_job_history(self, job_id: UUID) -> List[JobHistoryDTO]:
        stmt = (
            select(SearchSessionModel)
            .where(SearchSessionModel.job_requirement_id == job_id)
            .order_by(desc(SearchSessionModel.created_at))
        )
        result = await self.session.execute(stmt)
        sessions = result.scalars().all()
        
        return [
            JobHistoryDTO(
                id=s.id,
                created_at=s.created_at
            ) for s in sessions
        ]

