from src.application.agents.interfaces import Planner
from src.domain.agent_models import AgentObservation, AgentContext, AgentPlan

class RulePlanner(Planner):
    """Deterministic JSON-based decision tree planner."""
    async def plan(self, observation: AgentObservation, context: AgentContext) -> AgentPlan:
        # Map observation to predefined JSON actions
        return AgentPlan(steps=["step_1"])

class LLMPlanner(Planner):
    """Stub for LLM Reasoning (e.g. ReAct)"""
    async def plan(self, observation: AgentObservation, context: AgentContext) -> AgentPlan:
        pass

class TreeSearchPlanner(Planner):
    """Stub for Tree of Thoughts"""
    async def plan(self, observation: AgentObservation, context: AgentContext) -> AgentPlan:
        pass

class GraphPlanner(Planner):
    """Stub for Graph of Thoughts"""
    async def plan(self, observation: AgentObservation, context: AgentContext) -> AgentPlan:
        pass
