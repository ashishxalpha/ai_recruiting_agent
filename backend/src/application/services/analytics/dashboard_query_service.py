from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.dashboard import DashboardMetricsDTO

class DashboardQueryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_metrics(self) -> DashboardMetricsDTO:
        return DashboardMetricsDTO()
