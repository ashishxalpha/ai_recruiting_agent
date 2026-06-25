from typing import List
from uuid import UUID
from src.application.agents.interfaces import ReplayEngine
from src.domain.agent_models import ReasoningTrace

class EventStreamReplayEngine(ReplayEngine):
    async def replay_session(self, session_id: UUID) -> List[ReasoningTrace]:
        return []
