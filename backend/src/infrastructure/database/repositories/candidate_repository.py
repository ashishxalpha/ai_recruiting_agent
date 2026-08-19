from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import Candidate
from src.domain.interfaces.repositories import CandidateRepository
from src.infrastructure.database.models import (
    CandidateModel, CandidateSkillModel, CandidateEducationModel, 
    CandidateExperienceModel, CandidateProjectModel
)

class SQLAlchemyCandidateRepository(CandidateRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, candidate: Candidate) -> Candidate:
        db_model = CandidateModel(
            id=candidate.id,
            status=candidate.status,
            first_name=candidate.first_name,
            last_name=candidate.last_name,
            email=candidate.email,
            phone=candidate.phone,
            summary=candidate.summary,
            created_at=candidate.created_at,
            updated_at=candidate.updated_at
        )
        
        # Add relationships
        db_model.skills = [
            CandidateSkillModel(id=s.id, name=s.name, proficiency=s.proficiency) 
            for s in candidate.skills
        ]
        db_model.education = [
            CandidateEducationModel(
                id=e.id, institution=e.institution, degree=e.degree,
                field_of_study=e.field_of_study, start_date=e.start_date,
                end_date=e.end_date, description=e.description
            ) for e in candidate.education
        ]
        db_model.experience = [
            CandidateExperienceModel(
                id=e.id, company=e.company, title=e.title,
                start_date=e.start_date, end_date=e.end_date, description=e.description
            ) for e in candidate.experience
        ]
        db_model.projects = [
            CandidateProjectModel(
                id=p.id, name=p.name, description=p.description, url=p.url
            ) for p in candidate.projects
        ]

        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return candidate

    async def get_by_id(self, id: UUID) -> Optional[Candidate]:
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.id == id, CandidateModel.deleted_at == None)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        
        return Candidate(
            id=model.id,
            status=model.status,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone=model.phone,
            summary=model.summary,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_by_email(self, email: str) -> Optional[Candidate]:
        result = await self.session.execute(
            select(CandidateModel)
            .where(CandidateModel.email == email, CandidateModel.deleted_at == None)
            .order_by(CandidateModel.created_at.desc())
            .limit(1)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        
        return Candidate(
            id=model.id,
            status=model.status,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            phone=model.phone,
            summary=model.summary,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Candidate]:
        result = await self.session.execute(
            select(CandidateModel)
            .where(CandidateModel.deleted_at == None)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [
            Candidate(
                id=m.id,
                status=m.status,
                first_name=m.first_name,
                last_name=m.last_name,
                email=m.email,
                phone=m.phone,
                summary=m.summary,
                created_at=m.created_at,
                updated_at=m.updated_at
            ) for m in models
        ]

    async def update(self, candidate: Candidate) -> Candidate:
        from sqlalchemy import delete
        
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.id == candidate.id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.status = candidate.status
            model.first_name = candidate.first_name
            model.last_name = candidate.last_name
            model.email = candidate.email
            model.phone = candidate.phone
            model.summary = candidate.summary
            model.updated_at = candidate.updated_at
            
            # Wipe existing relationships
            await self.session.execute(delete(CandidateSkillModel).where(CandidateSkillModel.candidate_id == candidate.id))
            await self.session.execute(delete(CandidateEducationModel).where(CandidateEducationModel.candidate_id == candidate.id))
            await self.session.execute(delete(CandidateExperienceModel).where(CandidateExperienceModel.candidate_id == candidate.id))
            await self.session.execute(delete(CandidateProjectModel).where(CandidateProjectModel.candidate_id == candidate.id))
            
            # Recreate relationships
            for s in candidate.skills:
                self.session.add(CandidateSkillModel(id=s.id, candidate_id=candidate.id, name=s.name, proficiency=s.proficiency))
            for e in candidate.education:
                self.session.add(CandidateEducationModel(id=e.id, candidate_id=candidate.id, institution=e.institution, degree=e.degree, field_of_study=e.field_of_study, start_date=e.start_date, end_date=e.end_date, description=e.description))
            for e in candidate.experience:
                self.session.add(CandidateExperienceModel(id=e.id, candidate_id=candidate.id, company=e.company, title=e.title, start_date=e.start_date, end_date=e.end_date, description=e.description))
            for p in candidate.projects:
                self.session.add(CandidateProjectModel(id=p.id, candidate_id=candidate.id, name=p.name, description=p.description, url=p.url))
            
            await self.session.commit()
        return candidate

    async def delete(self, id: UUID) -> bool:
        from datetime import datetime
        result = await self.session.execute(
            select(CandidateModel).where(CandidateModel.id == id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.deleted_at = datetime.utcnow()
            await self.session.commit()
            return True
        return False
