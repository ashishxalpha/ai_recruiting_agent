from typing import Optional, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc, cast, String
from uuid import UUID
import math

from src.infrastructure.database.models import JobRequirementModel, CandidateModel
from src.application.schemas.pagination import PaginatedResponse
from src.application.schemas.job import JobSummaryDTO, JobDetailsDTO
from src.observability.tracing import get_tracer
from src.domain.enums import CandidateStatus

tracer = get_tracer(__name__)

class JobQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_jobs(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        department: Optional[str] = None,
        location: Optional[str] = None,
        employment_type: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> PaginatedResponse[JobSummaryDTO]:
        with tracer.start_as_current_span("JobQueryService.list_jobs"):
            # Base query
            stmt = select(JobRequirementModel).where(JobRequirementModel.deleted_at.is_(None))

            # Filtering
            if status:
                stmt = stmt.where(JobRequirementModel.status == status)
            if department:
                stmt = stmt.where(JobRequirementModel.department == department)
            if location:
                stmt = stmt.where(JobRequirementModel.location == location)
            if employment_type:
                stmt = stmt.where(JobRequirementModel.employment_type == employment_type)

            # Searching
            if search:
                search_term = f"%{search}%"
                stmt = stmt.where(
                    or_(
                        JobRequirementModel.title.ilike(search_term),
                        JobRequirementModel.department.ilike(search_term),
                        JobRequirementModel.hiring_manager.ilike(search_term)
                    )
                )

            # Count total
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = await self.session.scalar(count_stmt) or 0

            # Sorting
            sort_col = getattr(JobRequirementModel, sort_by, JobRequirementModel.created_at)

            if sort_order.lower() == "desc":
                stmt = stmt.order_by(desc(sort_col))
            else:
                stmt = stmt.order_by(asc(sort_col))

            # Pagination
            offset = (page - 1) * page_size
            stmt = stmt.offset(offset).limit(page_size)

            # Subqueries for counts
            from src.infrastructure.database.models import GroundTruthEventModel
            
            # Using lateral subqueries or scalar subqueries to avoid N+1
            candidate_count_sq = select(func.count(GroundTruthEventModel.id)).where(GroundTruthEventModel.job_requirement_id == JobRequirementModel.id).correlate(JobRequirementModel).scalar_subquery()
            shortlisted_count_sq = select(func.count(GroundTruthEventModel.id)).where(GroundTruthEventModel.job_requirement_id == JobRequirementModel.id, GroundTruthEventModel.recruiter_decision == 'SHORTLISTED').correlate(JobRequirementModel).scalar_subquery()
            interview_count_sq = select(func.count(GroundTruthEventModel.id)).where(GroundTruthEventModel.job_requirement_id == JobRequirementModel.id, GroundTruthEventModel.recruiter_decision == 'INTERVIEW').correlate(JobRequirementModel).scalar_subquery()
            hired_count_sq = select(func.count(GroundTruthEventModel.id)).where(GroundTruthEventModel.job_requirement_id == JobRequirementModel.id, GroundTruthEventModel.recruiter_decision == 'HIRED').correlate(JobRequirementModel).scalar_subquery()
            
            stmt = stmt.add_columns(
                candidate_count_sq.label("candidate_count"),
                shortlisted_count_sq.label("shortlisted_count"),
                interview_count_sq.label("interview_count"),
                hired_count_sq.label("hired_count")
            )

            result = await self.session.execute(stmt)
            rows = result.all()

            # Mapping to DTO
            items = []
            for row in rows:
                model = row[0]
                items.append(JobSummaryDTO(
                    id=model.id,
                    title=model.title,
                    department=model.department,
                    location=model.location,
                    employment_type=model.employment_type,
                    status=model.status,
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                    candidate_count=row.candidate_count or 0,
                    shortlisted_count=row.shortlisted_count or 0,
                    interview_count=row.interview_count or 0,
                    hired_count=row.hired_count or 0
                ))

            total_pages = math.ceil(total / page_size) if page_size else 0
            
            return PaginatedResponse[JobSummaryDTO](
                items=items,
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1
            )

    async def get_job_details(self, job_id: UUID) -> Optional[JobDetailsDTO]:
        with tracer.start_as_current_span("JobQueryService.get_job_details"):
            stmt = select(JobRequirementModel).where(
                JobRequirementModel.id == job_id, 
                JobRequirementModel.deleted_at.is_(None)
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if not model:
                return None
                
            return JobDetailsDTO.model_validate(model)
