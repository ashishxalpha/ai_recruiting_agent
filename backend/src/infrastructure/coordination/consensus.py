from uuid import UUID
from src.application.coordination.interfaces import ConsensusEngine
from src.domain.coordination_models import Consensus

class DefaultConsensusEngine(ConsensusEngine):
    async def evaluate(self, goal_id: UUID) -> Consensus:
        return Consensus(
            goal_id=goal_id,
            resolution="Agreed",
            achieved=True
        )
