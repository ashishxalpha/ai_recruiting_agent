from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from uuid import UUID

from src.presentation.api.dependencies import get_db_session
from src.application.services.analytics.realtime import RealtimeAnalyticsProvider

router = APIRouter()

@router.get("/jobs/{job_id}/analytics")
async def get_job_analytics(
    job_id: UUID,
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """Get matching and feedback analytics for a specific job."""
    provider = RealtimeAnalyticsProvider(db)
    return await provider.get_job_analytics(job_id)

@router.get("/analytics/evaluation")
async def get_evaluation_metrics(
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """Get system-wide evaluation metrics (e.g. agreement rate, approval rate, etc.)."""
    provider = RealtimeAnalyticsProvider(db)
    return await provider.get_evaluation_metrics()
