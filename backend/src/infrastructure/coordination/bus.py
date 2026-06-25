from typing import List, Dict
from uuid import UUID
from src.application.coordination.interfaces import AgentCommunicationBus
from src.domain.coordination_models import AgentMessage

class InMemoryCommunicationBus(AgentCommunicationBus):
    def __init__(self):
        self._topics: Dict[str, List[callable]] = {}

    async def send(self, message: AgentMessage) -> None:
        pass

    async def publish(self, topic: str, message: AgentMessage) -> None:
        if topic in self._topics:
            for handler in self._topics[topic]:
                await handler(message)

    async def broadcast(self, message: AgentMessage) -> None:
        pass

    async def reply(self, original_id: UUID, message: AgentMessage) -> None:
        pass

    async def subscribe(self, topic: str, handler: callable) -> None:
        if topic not in self._topics:
            self._topics[topic] = []
        self._topics[topic].append(handler)
