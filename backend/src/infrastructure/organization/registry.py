from typing import List
from uuid import UUID
from src.application.organization.interfaces import SkillRegistry
from src.domain.organization_models import AgentSkill

class DefaultSkillRegistry(SkillRegistry):
    def __init__(self):
        self._skills = {}

    async def register(self, skill: AgentSkill) -> None:
        self._skills[skill.id] = skill

    async def discover(self) -> List[AgentSkill]:
        return list(self._skills.values())

    async def search(self, query: str) -> List[AgentSkill]:
        return []

    async def execute(self, skill_id: UUID, payload: dict) -> dict:
        return {"status": "executed"}

    async def version(self, skill_id: UUID) -> str:
        return "1.0.0"
