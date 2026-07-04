from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from src.presentation.api.dependencies import get_db_session
from src.application.services.analytics.analytics_query_service import AnalyticsQueryService
from src.application.schemas.analytics import (
    AnalyticsResponseDTO,
    RecruitingFunnelDTO,
    MatchingAnalyticsDTO,
    WorkflowAnalyticsDTO,
    MemoryAnalyticsDTO,
    AgentAnalyticsDTO,
    ToolAnalyticsDTO,
    OrganizationAnalyticsDTO,
    PlatformHealthDTO
)

router = APIRouter()

def get_analytics_service(db: AsyncSession = Depends(get_db_session)) -> AnalyticsQueryService:
    return AnalyticsQueryService(db)

@router.get("/funnel", response_model=AnalyticsResponseDTO[RecruitingFunnelDTO])
async def get_funnel_metrics(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_funnel_metrics()

@router.get("/matching", response_model=AnalyticsResponseDTO[MatchingAnalyticsDTO])
async def get_matching_analytics(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_matching_analytics()

@router.get("/workflow", response_model=AnalyticsResponseDTO[WorkflowAnalyticsDTO])
async def get_workflow_analytics(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_workflow_analytics()

@router.get("/memory", response_model=AnalyticsResponseDTO[MemoryAnalyticsDTO])
async def get_memory_analytics(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_memory_analytics()

@router.get("/agent", response_model=AnalyticsResponseDTO[AgentAnalyticsDTO])
async def get_agent_analytics(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_agent_analytics()

@router.get("/tools", response_model=AnalyticsResponseDTO[ToolAnalyticsDTO])
async def get_tool_analytics(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_tool_analytics()

@router.get("/organization", response_model=AnalyticsResponseDTO[OrganizationAnalyticsDTO])
async def get_organization_analytics(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_organization_analytics()

@router.get("/health", response_model=AnalyticsResponseDTO[PlatformHealthDTO])
async def get_platform_health(service: AnalyticsQueryService = Depends(get_analytics_service)):
    return await service.get_platform_health()

# Keep legacy dashboard until fully replaced
from src.application.services.analytics.dashboard_query_service import DashboardQueryService
from src.application.schemas.dashboard import DashboardMetricsDTO

@router.get("/dashboard", response_model=DashboardMetricsDTO)
async def get_dashboard(db: AsyncSession = Depends(get_db_session)):
    service = DashboardQueryService(db)
    return await service.get_dashboard_metrics()
