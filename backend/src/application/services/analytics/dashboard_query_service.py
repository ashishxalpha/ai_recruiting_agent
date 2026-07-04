from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone

from src.infrastructure.database.models import (
    CandidateModel,
    JobRequirementModel,
    BackgroundJobModel,
    RecruiterFeedbackModel
)
from src.application.schemas.dashboard import (
    DashboardMetricsDTO,
    DashboardSummaryDTO,
    DashboardActivityDTO,
    DashboardHealthDTO
)
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class DashboardQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dashboard_metrics(self) -> DashboardMetricsDTO:
        with tracer.start_as_current_span("DashboardQueryService.get_dashboard_metrics"):
            # Execute summary counts
            candidates_count = await self._count(CandidateModel)
            jobs_count = await self._count(JobRequirementModel)
            workflows_count = await self._count(BackgroundJobModel)
            
            from src.infrastructure.database.models import CandidateMatchModel
            
            # Pending feedback is any CandidateMatch without a corresponding RecruiterFeedbackModel
            stmt_feedback = select(func.count(CandidateMatchModel.id)).where(
                CandidateMatchModel.id.not_in(
                    select(RecruiterFeedbackModel.candidate_match_id)
                )
            )
            feedback_count = await self.session.scalar(stmt_feedback) or 0

            # Activity counts (e.g. workflows today/this week)
            now = datetime.now(timezone.utc)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = today_start - timedelta(days=7)

            stmt_today = select(func.count(BackgroundJobModel.id)).where(BackgroundJobModel.created_at >= today_start)
            stmt_week = select(func.count(BackgroundJobModel.id)).where(BackgroundJobModel.created_at >= week_start)

            today_val = await self.session.scalar(stmt_today) or 0
            week_val = await self.session.scalar(stmt_week) or 0

            return DashboardMetricsDTO(
                summary=DashboardSummaryDTO(
                    candidates=candidates_count,
                    jobs=jobs_count,
                    workflows=workflows_count,
                    pending_feedback=feedback_count
                ),
                activity=DashboardActivityDTO(
                    today=today_val,
                    week=week_val
                ),
                health=DashboardHealthDTO(
                    agents="healthy",
                    tools="healthy"
                )
            )

    async def _count(self, model) -> int:
        stmt = select(func.count(model.id))
        result = await self.session.execute(stmt)
        return result.scalar_one() or 0
