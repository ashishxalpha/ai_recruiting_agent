from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Dict, Any

from src.application.services.memory.providers import (
    MemorySearchProvider,
    MemoryGraphProvider,
    MemoryTimelineProvider,
    MemoryRelationshipProvider,
    MemoryConsolidationProvider,
    MemoryStatisticsProvider,
    MemoryListProvider
)
from src.application.schemas.memory_explorer import (
    MemoryResponseDTO,
    MemoryListDTO,
    MemoryDetailsDTO,
    MemoryRetrievalDTO,
    MemoryGraphDTO,
    MemoryTimelineDTO,
    MemoryRelationshipListDTO,
    MemoryConsolidationDTO,
    MemoryStatisticsDTO
)

class MemoryQueryService:
    """Orchestrator for Memory Explorer read models. Delegates to domain-specific providers."""
    
    def __init__(self, session: AsyncSession):
        self.search_provider = MemorySearchProvider(session)
        self.graph_provider = MemoryGraphProvider(session)
        self.timeline_provider = MemoryTimelineProvider(session)
        self.relationship_provider = MemoryRelationshipProvider(session)
        self.consolidation_provider = MemoryConsolidationProvider(session)
        self.statistics_provider = MemoryStatisticsProvider(session)
        self.list_provider = MemoryListProvider(session)

    async def list_memories(self) -> MemoryResponseDTO[MemoryListDTO]:
        return await self.list_provider.list_memories()

    async def get_details(self, memory_id: UUID) -> MemoryResponseDTO[MemoryDetailsDTO]:
        return await self.list_provider.get_details(memory_id)

    async def search(self, query: str, filters: Dict[str, Any] = None) -> MemoryResponseDTO[MemoryRetrievalDTO]:
        return await self.search_provider.search(query, filters)

    async def get_graph(self) -> MemoryResponseDTO[MemoryGraphDTO]:
        return await self.graph_provider.get_graph()

    async def get_timeline(self, memory_id: UUID) -> MemoryResponseDTO[MemoryTimelineDTO]:
        return await self.timeline_provider.get_timeline(memory_id)

    async def get_relationships(self, memory_id: UUID) -> MemoryResponseDTO[MemoryRelationshipListDTO]:
        return await self.relationship_provider.get_relationships(memory_id)

    async def get_consolidations(self) -> MemoryResponseDTO[MemoryConsolidationDTO]:
        return await self.consolidation_provider.get_consolidations()

    async def get_statistics(self) -> MemoryResponseDTO[MemoryStatisticsDTO]:
        return await self.statistics_provider.get_statistics()
