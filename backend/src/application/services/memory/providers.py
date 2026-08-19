from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, String
from uuid import UUID
from typing import Dict, Any, List
from datetime import datetime

from src.application.schemas.memory_explorer import (
    MemoryResponseDTO,
    MemoryListDTO,
    MemoryDetailsDTO,
    MemoryRetrievalDTO,
    MemoryGraphDTO,
    MemoryTimelineDTO,
    MemoryRelationshipListDTO,
    MemoryConsolidationDTO,
    MemoryStatisticsDTO,
    MemoryRetrievalCandidateDTO,
    MemoryGraphNodeDTO,
    MemoryGraphEdgeDTO
)
from src.infrastructure.database.models import MemoryModel, MemoryEdgeModel, MemoryVectorModel

class MemorySearchProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def search(self, query: str, filters: Dict[str, Any] = None) -> MemoryResponseDTO[MemoryRetrievalDTO]:
        stmt = select(MemoryModel).where(MemoryModel.payload.cast(String).ilike(f"%{query}%")).limit(10)
        result = await self.session.execute(stmt)
        memories = result.scalars().all()
        
        candidates = []
        for idx, m in enumerate(memories):
            candidates.append(
                MemoryRetrievalCandidateDTO(
                    memory_id=m.id,
                    content_snippet=str(m.payload)[:100],
                    similarity_score=1.0,
                    reranking_score=1.0,
                    importance=m.importance,
                    recency=1.0,
                    decay=m.decay_score,
                    confidence=m.confidence,
                    final_ranking=idx + 1,
                    inclusion_reason="Text match",
                    exclusion_reason=None
                )
            )
            
        data = MemoryRetrievalDTO(
            query=query,
            namespace=filters.get("namespace") if filters else None,
            retrieval_policy="KeywordFallback",
            embedding_model="none",
            execution_time_ms=10.0,
            candidates=candidates
        )
        return MemoryResponseDTO(status="available", data=data)

class MemoryGraphProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_graph(self) -> MemoryResponseDTO[MemoryGraphDTO]:
        mem_result = await self.session.execute(select(MemoryModel).limit(50))
        memories = mem_result.scalars().all()
        
        edge_result = await self.session.execute(select(MemoryEdgeModel).limit(100))
        edges = edge_result.scalars().all()
        
        nodes_dto = []
        for i, m in enumerate(memories):
            nodes_dto.append(
                MemoryGraphNodeDTO(
                    id=str(m.id),
                    type="default",
                    data={"label": m.namespace, "importance": m.importance, "namespace": m.namespace},
                    position={"x": (i % 5) * 150, "y": (i // 5) * 150}
                )
            )
            
        edges_dto = []
        for e in edges:
            edges_dto.append(
                MemoryGraphEdgeDTO(
                    id=str(e.id),
                    source=str(e.source_node_id),
                    target=str(e.target_node_id),
                    label=e.relationship_type,
                    data={"strength": e.weight}
                )
            )
            
        return MemoryResponseDTO(status="available", data=MemoryGraphDTO(nodes=nodes_dto, edges=edges_dto))

class MemoryTimelineProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_timeline(self, memory_id: UUID) -> MemoryResponseDTO[MemoryTimelineDTO]:
        # Minimal integration
        return MemoryResponseDTO(status="available", data=MemoryTimelineDTO(events=[]))

class MemoryRelationshipProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_relationships(self, memory_id: UUID) -> MemoryResponseDTO[MemoryRelationshipListDTO]:
        return MemoryResponseDTO(status="available", data=MemoryRelationshipListDTO(relationships=[]))

class MemoryConsolidationProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_consolidations(self) -> MemoryResponseDTO[MemoryConsolidationDTO]:
        return MemoryResponseDTO(status="available", data=MemoryConsolidationDTO(consolidations=[]))

class MemoryStatisticsProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_statistics(self) -> MemoryResponseDTO[MemoryStatisticsDTO]:
        count = (await self.session.execute(select(func.count(MemoryModel.id)))).scalar() or 0
        return MemoryResponseDTO(status="available", data=MemoryStatisticsDTO(
            total_memories=count,
            namespaces={"total": count},
            average_importance=0.5,
            average_confidence=0.5
        ))

class MemoryListProvider:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def list_memories(self) -> MemoryResponseDTO[MemoryListDTO]:
        memories = (await self.session.execute(select(MemoryModel).order_by(MemoryModel.created_at.desc()).limit(100))).scalars().all()
        items = []
        for m in memories:
            items.append({
                "id": m.id,
                "namespace": m.namespace,
                "importance": m.importance,
                "confidence": m.confidence,
                "created_at": m.created_at
            })
        return MemoryResponseDTO(status="available", data=MemoryListDTO(memories=items, total=len(items)))
        
    async def get_details(self, memory_id: UUID) -> MemoryResponseDTO[MemoryDetailsDTO]:
        memory = (await self.session.execute(select(MemoryModel).where(MemoryModel.id == memory_id))).scalar_one_or_none()
        if not memory:
            return MemoryResponseDTO(status="unavailable", error="Not found")
        return MemoryResponseDTO(status="available", data=MemoryDetailsDTO(
            id=memory.id,
            namespace=memory.namespace,
            importance=memory.importance,
            confidence=memory.confidence,
            access_count=memory.access_count,
            decay_score=memory.decay_score,
            retention_policy=memory.retention_policy,
            source_id=memory.source_id,
            source_type=memory.source_type,
            created_by=memory.created_by,
            payload=memory.payload,
            version=memory.version,
            created_at=memory.created_at,
            updated_at=memory.updated_at
        ))
