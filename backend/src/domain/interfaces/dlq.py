from typing import Protocol, Any, Dict
from uuid import UUID

class FailedExtractionTrackingProvider(Protocol):
    """
    Abstraction for tracking failed extractions in a Dead Letter Queue (DLQ).
    This allows recovering, analyzing, or manually triggering retries for documents
    that failed processing due to parsing, AI model errors, or validation issues.
    """
    async def track_failure(self, document_id: UUID, error_type: str, error_message: str, payload: Dict[str, Any] = None) -> None:
        """Track a failed extraction."""
        ...
        
    async def get_failed_extractions(self, limit: int = 100, offset: int = 0) -> list:
        """Retrieve a list of failed extractions for review."""
        ...
