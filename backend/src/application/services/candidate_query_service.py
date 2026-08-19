from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from src.application.schemas.candidate import CandidateSummaryDTO, CandidateDetailsDTO
from src.application.schemas.pagination import PaginatedResponse

class CandidateQueryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_candidates(
        self, 
        page: int, 
        page_size: int, 
        search: Optional[str] = None, 
        status: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> PaginatedResponse[CandidateSummaryDTO]:
        from sqlalchemy import select, func, desc, asc
        from src.infrastructure.database.models import CandidateModel
        from src.domain.enums import CandidateStatus
        
        # 1. Base query
        stmt = select(CandidateModel)
        count_stmt = select(func.count(CandidateModel.id))
        
        # 2. Filters
        if status:
            try:
                status_enum = CandidateStatus(status)
                stmt = stmt.where(CandidateModel.status == status_enum)
                count_stmt = count_stmt.where(CandidateModel.status == status_enum)
            except ValueError:
                pass
                
        if search:
            search_pattern = f"%{search}%"
            # Simple search on name or email
            stmt = stmt.where(
                (CandidateModel.first_name.ilike(search_pattern)) | 
                (CandidateModel.last_name.ilike(search_pattern)) |
                (CandidateModel.email.ilike(search_pattern))
            )
            count_stmt = count_stmt.where(
                (CandidateModel.first_name.ilike(search_pattern)) | 
                (CandidateModel.last_name.ilike(search_pattern)) |
                (CandidateModel.email.ilike(search_pattern))
            )
            
        # 3. Total count
        total = (await self.db.execute(count_stmt)).scalar() or 0
        total_pages = max(1, (total + page_size - 1) // page_size)
        
        # 4. Sorting
        sort_col = getattr(CandidateModel, sort_by, CandidateModel.created_at)
        if sort_order.lower() == "desc":
            stmt = stmt.order_by(desc(sort_col))
        else:
            stmt = stmt.order_by(asc(sort_col))
            
        # 5. Pagination
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        
        # 6. Execute
        result = await self.db.execute(stmt)
        candidates = result.scalars().all()
        
        # 7. Map to DTO
        items = []
        for c in candidates:
            items.append(CandidateSummaryDTO(
                id=c.id,
                full_name=f"{c.first_name or ''} {c.last_name or ''}".strip() or "Unknown Candidate",
                email=c.email,
                current_status=c.status.value,
                profile_quality=0.0,
                created_at=c.created_at,
                updated_at=c.updated_at
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

    async def get_candidate_details(self, id: UUID) -> Optional[CandidateDetailsDTO]:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        from src.infrastructure.database.models import CandidateModel
        from src.application.schemas.candidate import (
            CandidateProfileDTO,
            CandidateSkillDTO,
            CandidateExperienceDTO,
            CandidateEducationDTO,
            CandidateProjectDTO
        )

        stmt = select(CandidateModel).where(CandidateModel.id == id).options(
            selectinload(CandidateModel.skills),
            selectinload(CandidateModel.experience),
            selectinload(CandidateModel.education),
            selectinload(CandidateModel.projects)
        )
        result = await self.db.execute(stmt)
        c = result.scalar_one_or_none()

        if not c:
            return None

        profile = CandidateProfileDTO(
            id=c.id,
            status=c.status.value,
            first_name=c.first_name,
            last_name=c.last_name,
            email=c.email,
            phone=c.phone,
            summary=c.summary,
            created_at=c.created_at,
            updated_at=c.updated_at
        )

        skills = [CandidateSkillDTO(id=s.id, name=s.name, proficiency=s.proficiency) for s in c.skills]
        experience = [CandidateExperienceDTO(
            id=e.id, company=e.company, title=e.title, start_date=e.start_date, end_date=e.end_date, description=e.description
        ) for e in c.experience]
        education = [CandidateEducationDTO(
            id=e.id, institution=e.institution, degree=e.degree, field_of_study=e.field_of_study, start_date=e.start_date, end_date=e.end_date, description=e.description
        ) for e in c.education]
        projects = [CandidateProjectDTO(
            id=p.id, name=p.name, description=p.description, url=p.url
        ) for p in c.projects]

        return CandidateDetailsDTO(
            profile=profile,
            skills=skills,
            experience=experience,
            education=education,
            projects=projects
        )
