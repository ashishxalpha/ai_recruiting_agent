from src.application.coordination.interfaces import ConflictResolver
from src.domain.coordination_models import Conflict

class DefaultConflictResolver(ConflictResolver):
    async def resolve(self, conflict: Conflict) -> str:
        return "RESOLVED"
