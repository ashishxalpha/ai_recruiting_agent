from src.application.coordination.interfaces import CoordinationStrategy
from src.domain.coordination_models import DelegationPlan

class SequentialStrategy(CoordinationStrategy):
    async def execute(self, plan: DelegationPlan) -> None:
        raise NotImplementedError("feature_available: false")

class ParallelStrategy(CoordinationStrategy):
    async def execute(self, plan: DelegationPlan) -> None:
        raise NotImplementedError("feature_available: false")

class HierarchicalStrategy(CoordinationStrategy):
    async def execute(self, plan: DelegationPlan) -> None:
        raise NotImplementedError("feature_available: false")
