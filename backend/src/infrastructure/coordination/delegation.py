from typing import List
from src.application.coordination.interfaces import DelegationPlanner, DelegationEngine
from src.domain.coordination_models import GoalNode, DelegationPlan, DelegationTask

class DefaultDelegationPlanner(DelegationPlanner):
    async def create_plan(self, nodes: List[GoalNode]) -> DelegationPlan:
        if not nodes:
            return DelegationPlan(goal_id="00000000-0000-0000-0000-000000000000")
            
        goal_id = nodes[0].goal_id
        plan = DelegationPlan(goal_id=goal_id)
        
        for node in nodes:
            plan.tasks.append(DelegationTask(goal_node_id=node.id, payload=node.payload))
            
        return plan

class DefaultDelegationEngine(DelegationEngine):
    async def assign_plan(self, plan: DelegationPlan) -> None:
        import uuid
        
        # Assign to the primary recruiting agent by default
        CORE_AGENT_UUID = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
        
        for task in plan.tasks:
            task.assigned_agent_id = CORE_AGENT_UUID
            task.status = "ASSIGNED"
