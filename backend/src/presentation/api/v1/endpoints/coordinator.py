from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from uuid import UUID

from src.presentation.api.dependencies import get_db_session
from src.application.schemas.common import StandardResponseDTO
from src.application.schemas.coordination import (
    CoordinationSessionDTO, CoordinationConsensusDTO,
    CoordinationHandoffDTO, CoordinationConflictDTO
)
from src.application.services.coordination.coordination_query_service import CoordinationQueryService

router = APIRouter()

def get_coord_service(db: AsyncSession = Depends(get_db_session)) -> CoordinationQueryService:
    return CoordinationQueryService(db)

@router.get("", response_model=StandardResponseDTO[List[Dict[str, Any]]])
async def get_overview(service: CoordinationQueryService = Depends(get_coord_service)):
    return await service.get_overview()

@router.get("/sessions", response_model=StandardResponseDTO[List[CoordinationSessionDTO]])
async def list_sessions(service: CoordinationQueryService = Depends(get_coord_service)):
    return await service.get_sessions()

@router.get("/consensus", response_model=StandardResponseDTO[List[CoordinationConsensusDTO]])
async def get_consensus(service: CoordinationQueryService = Depends(get_coord_service)):
    return await service.get_consensus()

@router.get("/handoffs", response_model=StandardResponseDTO[List[CoordinationHandoffDTO]])
async def get_handoffs(service: CoordinationQueryService = Depends(get_coord_service)):
    return await service.get_handoffs()

@router.get("/conflicts", response_model=StandardResponseDTO[List[CoordinationConflictDTO]])
async def get_conflicts(service: CoordinationQueryService = Depends(get_coord_service)):
    return await service.get_conflicts()


# Write operations kept for compatibility
@router.post("/start")
async def start_coordination(request: Dict[str, Any]) -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.post("/pause")
async def pause_coordination() -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.post("/resume")
async def resume_coordination() -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")

@router.post("/cancel")
async def cancel_coordination() -> Any:
    raise HTTPException(status_code=501, detail="feature_available: false")
