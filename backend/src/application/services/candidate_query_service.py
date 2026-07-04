from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc
from uuid import UUID
from datetime import datetime
import math

from src.infrastructure.database.models import CandidateModel, AIExtractionModel, ResumeIngestionRequestModel
from src.application.schemas.pagination import PaginatedResponse
from src.application.schemas.candidate import (
    CandidateSummaryDTO, 
    CandidateDetailsDTO, 
    CandidateProfileDTO,
    CandidateSkillDTO,
    CandidateExperienceDTO,
    CandidateEducationDTO,
    CandidateProjectDTO
)
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class CandidateQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_candidates(
        self, 
        page: int = 1, 
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> PaginatedResponse[CandidateSummaryDTO]:
        with tracer.start_as_current_span("CandidateQueryService.list_candidates"):
            # Base query
            stmt = select(CandidateModel).where(CandidateModel.deleted_at.is_(None))

            # Filtering
            if status:
                stmt = stmt.where(CandidateModel.status == status)

            # Searching
            if search:
                search_term = f"%{search}%"
                stmt = stmt.where(
                    or_(
                        func.concat(CandidateModel.first_name, ' ', CandidateModel.last_name).ilike(search_term),
                        CandidateModel.email.ilike(search_term),
                        CandidateModel.phone.ilike(search_term)
                    )
                )

            # Counting total (before pagination)
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = await self.session.scalar(count_stmt) or 0

            # Sorting
            sort_col = getattr(CandidateModel, sort_by, CandidateModel.created_at)
            if sort_order.lower() == "desc":
                stmt = stmt.order_by(desc(sort_col))
            else:
                stmt = stmt.order_by(asc(sort_col))

            # Pagination
            offset = (page - 1) * page_size
            stmt = stmt.offset(offset).limit(page_size)

            result = await self.session.execute(stmt)
            models = result.scalars().all()

            # Mapping to DTO
            items = []
            for model in models:
                full_name = f"{model.first_name or ''} {model.last_name or ''}".strip() or "Unknown Candidate"
                # Workflow status and extraction confidence omitted from list view for performance; 
                # fetch via detail endpoints.
                items.append(CandidateSummaryDTO(
                    id=model.id,
                    full_name=full_name,
                    email=model.email,
                    phone=model.phone,
                    current_status=str(model.status.value) if hasattr(model.status, 'value') else str(model.status),
                    profile_quality=0.0, # Will be aggregated dynamically if needed
                    latest_workflow_status=None,
                    latest_extraction_confidence=None,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                ))

            total_pages = math.ceil(total / page_size) if page_size else 0
            
            return PaginatedResponse[CandidateSummaryDTO](
                items=items,
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1
            )

    async def get_candidate_details(self, candidate_id: UUID) -> Optional[CandidateDetailsDTO]:
        with tracer.start_as_current_span("CandidateQueryService.get_candidate_details"):
            from sqlalchemy.orm import selectinload
            
            stmt = (
                select(CandidateModel)
                .options(
                    selectinload(CandidateModel.skills),
                    selectinload(CandidateModel.experience),
                    selectinload(CandidateModel.education),
                    selectinload(CandidateModel.projects)
                )
                .where(CandidateModel.id == candidate_id, CandidateModel.deleted_at.is_(None))
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if not model:
                return None
                
            return CandidateDetailsDTO(
                profile=CandidateProfileDTO.model_validate(model),
                skills=[CandidateSkillDTO.model_validate(s) for s in model.skills],
                experience=[CandidateExperienceDTO.model_validate(e) for e in model.experience],
                education=[CandidateEducationDTO.model_validate(e) for e in model.education],
                projects=[CandidateProjectDTO.model_validate(p) for p in model.projects]
            )
