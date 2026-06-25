from typing import List, Any
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import AuditLog
from src.domain.interfaces.repositories import AuditRepository
from src.infrastructure.database.models import AuditLogModel
from datetime import datetime

class SQLAlchemyAuditRepository(AuditRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_action(self, entity_type: str, entity_id: UUID, action: str, changes: dict[str, Any]) -> AuditLog:
        new_id = uuid4()
        db_model = AuditLogModel(
            id=new_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            changes=changes,
        )
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        
        return AuditLog(
            id=db_model.id,
            entity_type=db_model.entity_type,
            entity_id=db_model.entity_id,
            action=db_model.action,
            changes=db_model.changes,
            created_at=db_model.created_at
        )

    async def get_by_entity(self, entity_type: str, entity_id: UUID) -> List[AuditLog]:
        result = await self.session.execute(
            select(AuditLogModel).where(
                AuditLogModel.entity_type == entity_type,
                AuditLogModel.entity_id == entity_id
            ).order_by(AuditLogModel.created_at.desc())
        )
        models = result.scalars().all()
        return [
            AuditLog(
                id=m.id,
                entity_type=m.entity_type,
                entity_id=m.entity_id,
                action=m.action,
                changes=m.changes,
                created_at=m.created_at
            ) for m in models
        ]
