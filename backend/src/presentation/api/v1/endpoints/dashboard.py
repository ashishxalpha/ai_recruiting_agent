from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.api.dependencies import get_db_session

from src.application.schemas.common import StandardResponseDTO
from src.application.schemas.dashboard import DashboardSummaryDTO, DashboardHealthDTO, RecentActivityDTO
from src.application.services.dashboard.dashboard_query_service import DashboardQueryService
from src.application.services.dashboard.recent_activity_query_service import RecentActivityQueryService

router = APIRouter()

def get_dashboard_service(db: AsyncSession = Depends(get_db_session)) -> DashboardQueryService:
    return DashboardQueryService(db)

def get_activity_service(db: AsyncSession = Depends(get_db_session)) -> RecentActivityQueryService:
    return RecentActivityQueryService(db)

@router.get("/summary", response_model=StandardResponseDTO[DashboardSummaryDTO])
async def get_dashboard_summary(service: DashboardQueryService = Depends(get_dashboard_service)):
    return await service.get_summary()

@router.get("/health", response_model=StandardResponseDTO[DashboardHealthDTO])
async def get_dashboard_health(service: DashboardQueryService = Depends(get_dashboard_service)):
    return await service.get_health()

@router.get("/activity", response_model=StandardResponseDTO[RecentActivityDTO])
async def get_recent_activity(
    limit: int = 20, 
    service: RecentActivityQueryService = Depends(get_activity_service)
):
    return await service.get_recent_activity(limit)
