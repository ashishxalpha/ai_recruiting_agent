from typing import List, Optional
from uuid import UUID
from src.application.coordination.interfaces import AgentMailbox
from src.domain.coordination_models import AgentMessage, AgentMailboxModel

class InMemoryAgentMailbox(AgentMailbox):
    def __init__(self, agent_id: UUID):
        self.model = AgentMailboxModel(agent_id=agent_id)

    async def enqueue(self, message: AgentMessage) -> None:
        self.model.messages.append(message)

    async def dequeue(self) -> Optional[AgentMessage]:
        if self.model.messages:
            return self.model.messages.pop(0)
        return None

    async def peek(self) -> Optional[AgentMessage]:
        if self.model.messages:
            return self.model.messages[0]
        return None

    async def archive(self, message_id: UUID) -> None:
        pass

    async def get_messages(self) -> List[AgentMessage]:
        return list(self.model.messages)
