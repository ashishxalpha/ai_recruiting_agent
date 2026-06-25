from typing import List, Optional, Dict
from uuid import UUID
from src.application.agents.interfaces import AgentRegistry, AgentTemplateRegistry
from src.domain.agent_models import Agent, AgentTemplate

class InMemoryAgentRegistry(AgentRegistry):
    def __init__(self):
        self._agents: Dict[UUID, Agent] = {}

    async def register(self, agent: Agent) -> None:
        self._agents[agent.id] = agent

    async def get(self, agent_id: UUID) -> Optional[Agent]:
        return self._agents.get(agent_id)

    async def list(self) -> List[Agent]:
        return list(self._agents.values())

class InMemoryTemplateRegistry(AgentTemplateRegistry):
    def __init__(self):
        self._templates: Dict[UUID, AgentTemplate] = {}

    async def register(self, template: AgentTemplate) -> None:
        self._templates[template.id] = template

    async def get(self, template_id: UUID) -> Optional[AgentTemplate]:
        return self._templates.get(template_id)
