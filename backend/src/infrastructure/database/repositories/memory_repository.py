from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.sql import func
from sqlalchemy.orm.exc import StaleDataError

from src.domain.interfaces.memory_repository import MemoryMetadataRepository, MemoryVectorRepository, WorkingMemoryStore
from src.domain.memory_models import BaseMemory, WorkingMemory, SemanticMemory, EpisodicMemory, ProceduralMemory, MemorySource
from src.infrastructure.database.models import MemoryModel, MemoryVectorModel, WorkingMemoryModel
import json

class SQLAlchemyMemoryMetadataRepository(MemoryMetadataRepository):
    """
    SQLAlchemy implementation of MemoryMetadataRepository with optimistic locking.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, memory: BaseMemory) -> BaseMemory:
        payload = memory.model_dump(mode="json", exclude={"id", "namespace", "importance", "confidence", "access_count", "decay_score", "retention_policy", "external_reference", "source"})
        
        # Check if memory exists
        result = await self.db.execute(select(MemoryModel).where(MemoryModel.id == memory.id))
        db_memory = result.scalars().first()

        if db_memory:
            # Update existing
            db_memory.namespace = memory.namespace.value
            db_memory.importance = memory.importance
            db_memory.confidence = memory.confidence
            db_memory.access_count = memory.access_count
            db_memory.decay_score = memory.decay_score
            db_memory.retention_policy = memory.retention_policy.value
            db_memory.external_reference = memory.external_reference
            db_memory.payload = payload
            
            try:
                # Flush to trigger optimistic locking version check
                await self.db.flush()
            except StaleDataError:
                raise ValueError(f"Concurrent update detected for memory {memory.id}. Please retry.")
        else:
            # Insert new
            db_memory = MemoryModel(
                id=memory.id,
                namespace=memory.namespace.value,
                importance=memory.importance,
                confidence=memory.confidence,
                access_count=memory.access_count,
                decay_score=memory.decay_score,
                retention_policy=memory.retention_policy.value,
                external_reference=memory.external_reference,
                source_id=memory.source.source_id,
                source_type=memory.source.source_type,
                created_by=memory.source.created_by,
                payload=payload
            )
            self.db.add(db_memory)
            await self.db.flush()
            
        return memory

    async def get(self, memory_id: UUID) -> Optional[BaseMemory]:
        result = await self.db.execute(select(MemoryModel).where(MemoryModel.id == memory_id, MemoryModel.deleted_at.is_(None)))
        db_memory = result.scalars().first()
        
        if not db_memory:
            return None
            
        # Reconstruct based on namespace, assuming namespace defines subclass
        # This is simplified. In a robust system, you'd have a factory.
        source = MemorySource(
            source_id=db_memory.source_id,
            source_type=db_memory.source_type,
            created_by=db_memory.created_by
        )
        
        base_data = {
            "id": db_memory.id,
            "namespace": db_memory.namespace,
            "importance": db_memory.importance,
            "confidence": db_memory.confidence,
            "access_count": db_memory.access_count,
            "decay_score": db_memory.decay_score,
            "retention_policy": db_memory.retention_policy,
            "external_reference": db_memory.external_reference,
            "source": source
        }
        
        # Merge payload
        base_data.update(db_memory.payload)
        
        if db_memory.namespace == "SEMANTIC":
            return SemanticMemory(**base_data)
        elif db_memory.namespace == "EPISODIC":
            return EpisodicMemory(**base_data)
        elif db_memory.namespace == "PROCEDURAL":
            return ProceduralMemory(**base_data)
            
        return BaseMemory(**base_data)

    async def delete(self, memory_id: UUID) -> None:
        await self.db.execute(update(MemoryModel).where(MemoryModel.id == memory_id).values(deleted_at=select(func.now()).scalar_subquery()))

    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> List[BaseMemory]:
        stmt = select(MemoryModel).where(MemoryModel.deleted_at.is_(None))
        for key, value in filters.items():
             stmt = stmt.where(MemoryModel.payload[key].astext == str(value))
        
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        # Simplified return, would normally deserialize
        return []

class SQLAlchemyMemoryVectorRepository(MemoryVectorRepository):
    """
    SQLAlchemy implementation of MemoryVectorRepository using pgvector.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def upsert_embedding(self, memory_id: UUID, embedding: List[float], model: str, version: str, content_hash: str) -> None:
        result = await self.db.execute(select(MemoryVectorModel).where(MemoryVectorModel.memory_id == memory_id))
        db_vector = result.scalars().first()
        
        if db_vector:
            db_vector.embedding_model = model
            db_vector.embedding_version = version
            db_vector.content_hash = content_hash
            db_vector.vector_data = embedding
        else:
            db_vector = MemoryVectorModel(
                memory_id=memory_id,
                embedding_model=model,
                embedding_dimension=len(embedding),
                embedding_version=version,
                content_hash=content_hash,
                vector_data=embedding
            )
            self.db.add(db_vector)
            
        await self.db.flush()
        
    async def delete_embedding(self, memory_id: UUID) -> None:
        await self.db.execute(delete(MemoryVectorModel).where(MemoryVectorModel.memory_id == memory_id))
        
    async def search(self, query_embedding: List[float], filters: Dict[str, Any], limit: int) -> List[UUID]:
        # Perform cosine distance search
        stmt = select(MemoryVectorModel.memory_id).order_by(MemoryVectorModel.vector_data.cosine_distance(query_embedding)).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())


class PostgresWorkingMemoryStore(WorkingMemoryStore):
    """
    Implementation of WorkingMemoryStore using PostgreSQL (JSONB).
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def set_state(self, session_id: UUID, state: WorkingMemory) -> None:
        result = await self.db.execute(select(WorkingMemoryModel).where(WorkingMemoryModel.session_id == session_id))
        db_wm = result.scalars().first()
        
        payload = state.model_dump(mode="json")
        
        if db_wm:
            db_wm.volatile_state = payload
        else:
            db_wm = WorkingMemoryModel(
                session_id=session_id,
                volatile_state=payload
            )
            self.db.add(db_wm)
            
        await self.db.flush()

    async def get_state(self, session_id: UUID) -> Optional[WorkingMemory]:
        result = await self.db.execute(select(WorkingMemoryModel).where(WorkingMemoryModel.session_id == session_id))
        db_wm = result.scalars().first()
        
        if not db_wm:
            return None
            
        return WorkingMemory(**db_wm.volatile_state)

    async def clear_state(self, session_id: UUID) -> None:
        await self.db.execute(delete(WorkingMemoryModel).where(WorkingMemoryModel.session_id == session_id))
