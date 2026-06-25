from uuid import UUID
from src.application.agents.interfaces import RuntimeScheduler
from src.domain.agent_models import AgentContext

class AsyncRuntimeScheduler(RuntimeScheduler):
    async def queue_execution(self, agent_id: UUID, context: AgentContext) -> None:
        pass

    async def prioritize(self, agent_id: UUID, priority: int) -> None:
        pass
