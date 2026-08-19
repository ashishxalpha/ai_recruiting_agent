from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List
from uuid import UUID

from src.presentation.api.dependencies import get_db_session
from src.application.services.memory.memory_query_service import MemoryQueryService
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

router = APIRouter()

def get_memory_query_service(db: AsyncSession = Depends(get_db_session)) -> MemoryQueryService:
    return MemoryQueryService(db)

# --- Write Operations (Memory Engine) ---

@router.post("")
async def create_memory(request: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    # Delegate to MemoryEngine.store()
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.patch("/{memory_id}")
async def update_memory(
    memory_id: UUID,
    request: Dict[str, Any],
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: UUID,
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.post("/consolidate")
async def trigger_consolidation(db: AsyncSession = Depends(get_db_session)
) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")


# --- Read Operations (Memory Explorer Observability) ---

@router.get("", response_model=MemoryResponseDTO[MemoryListDTO])
async def list_memories(
    namespace: str = Query(None),
    limit: int = 50,
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """List memory summaries."""
    return await service.list_memories()

@router.get("/graph", response_model=MemoryResponseDTO[MemoryGraphDTO])
async def get_memory_graph(
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """Get backend-owned memory graph topology for UI rendering."""
    return await service.get_graph()

@router.get("/statistics", response_model=MemoryResponseDTO[MemoryStatisticsDTO])
async def get_memory_statistics(
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """Get aggregated memory statistics."""
    return await service.get_statistics()

@router.get("/consolidations", response_model=MemoryResponseDTO[MemoryConsolidationDTO])
async def get_memory_consolidations(
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """Get consolidation event history."""
    return await service.get_consolidations()

@router.post("/search", response_model=MemoryResponseDTO[MemoryRetrievalDTO])
async def search_memory(request: Dict[str, Any],
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """Retrieval Debugger endpoint explaining semantic ranking decisions."""
    query = request.get("query", "")
    filters = request.get("filters", {})
    return await service.search(query, filters)

@router.get("/{memory_id}", response_model=MemoryResponseDTO[MemoryDetailsDTO])
async def get_memory_details(
    memory_id: UUID,
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """Get specific memory metadata."""
    return await service.get_details(memory_id)

@router.get("/{memory_id}/timeline", response_model=MemoryResponseDTO[MemoryTimelineDTO])
async def get_memory_timeline(
    memory_id: UUID,
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """Get lifecycle transitions (Created, Retrieved, Consolidated)."""
    return await service.get_timeline(memory_id)

@router.get("/{memory_id}/relationships", response_model=MemoryResponseDTO[MemoryRelationshipListDTO])
async def get_memory_relationships(
    memory_id: UUID,
    service: MemoryQueryService = Depends(get_memory_query_service)
):
    """Get memory edge relationships."""
    return await service.get_relationships(memory_id)
