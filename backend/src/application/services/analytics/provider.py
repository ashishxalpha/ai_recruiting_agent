from abc import ABC, abstractmethod
from typing import Dict, Any
from uuid import UUID

class AnalyticsProvider(ABC):
    @abstractmethod
    async def get_job_analytics(self, job_id: UUID) -> Dict[str, Any]:
        """Get high-level analytics for a specific job."""
        pass

    @abstractmethod
    async def get_evaluation_metrics(self) -> Dict[str, Any]:
        """Get system-wide evaluation metrics."""
        pass
