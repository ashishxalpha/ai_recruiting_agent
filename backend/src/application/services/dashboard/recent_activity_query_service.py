from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.common import StandardResponseDTO, create_response
from src.application.schemas.dashboard import RecentActivityDTO

class RecentActivityQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_recent_activity(self, limit: int = 20) -> StandardResponseDTO[RecentActivityDTO]:
        # Connects to the global EventBus persistence / audit table.
        # Since global event persistence is not yet fully modeled, return empty.
        data = RecentActivityDTO(activities=[])
        return create_response(
            data=data,
            feature_available=True,
            data_available=False,
            message="No recent activity found."
        )
