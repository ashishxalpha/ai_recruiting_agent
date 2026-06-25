from typing import List
from uuid import UUID
from src.application.coordination.interfaces import GoalEngine
from src.domain.coordination_models import Goal, GoalNode

class DefaultGoalEngine(GoalEngine):
    async def decompose(self, goal: Goal) -> List[GoalNode]:
        # Stub implementation mapping a single goal to a single node
        node = GoalNode(goal_id=goal.id, payload={"description": goal.description})
        return [node]

    async def get_dependencies(self, node_id: UUID) -> List[UUID]:
        return []
