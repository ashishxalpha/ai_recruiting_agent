from uuid import UUID
from src.application.coordination.interfaces import Supervisor, GoalEngine, DelegationPlanner, DelegationEngine, ConsensusEngine
from src.domain.coordination_models import Goal

class DefaultSupervisor(Supervisor):
    def __init__(self, goal_engine: GoalEngine, planner: DelegationPlanner, delegation_engine: DelegationEngine, consensus: ConsensusEngine):
        self.goal_engine = goal_engine
        self.planner = planner
        self.delegation_engine = delegation_engine
        self.consensus = consensus

    async def receive_goal(self, goal: Goal) -> None:
        nodes = await self.goal_engine.decompose(goal)
        plan = await self.planner.create_plan(nodes)
        await self.delegation_engine.assign_plan(plan)

    async def trigger_consensus(self, goal_id: UUID) -> None:
        await self.consensus.evaluate(goal_id)
