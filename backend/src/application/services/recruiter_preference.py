from abc import ABC, abstractmethod
from uuid import UUID
from typing import Any

class RecruiterPreferenceService(ABC):
    """
    Interface for future memory systems to learn recruiter preferences 
    based on feedback data. No implementation required in Sprint 6.
    """
    
    @abstractmethod
    async def learn_from_feedback(self, search_session_id: UUID, feedback_id: UUID) -> None:
        """Process recruiter feedback to learn their preferences."""
        pass

    @abstractmethod
    async def get_preferences(self, job_requirement_id: UUID) -> Any:
        """Retrieve learned preferences for a given job/recruiter."""
        pass
