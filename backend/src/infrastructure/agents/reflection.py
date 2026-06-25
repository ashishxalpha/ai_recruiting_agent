from src.application.agents.interfaces import ReflectionEngine
from src.domain.agent_models import ReasoningTrace, AgentContext, AgentReflection

class RuleReflectionEngine(ReflectionEngine):
    async def reflect(self, trace: ReasoningTrace, context: AgentContext) -> AgentReflection:
        return AgentReflection(
            summary="Executed rule based action.",
            success_rating=1.0,
            learnings=["Action completed successfully"]
        )
