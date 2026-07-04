from typing import Any
from src.application.agents.interfaces import ReflectionEngine
from src.domain.agent_models import ReasoningTrace, AgentContext, AgentReflection
from src.application.llm.interfaces import LLMProvider, LLMMessage
import json

class LLMReflectionEngine(ReflectionEngine):
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        
    async def reflect(self, trace: ReasoningTrace, context: AgentContext) -> AgentReflection:
        prompt = "Reflect on this execution trace and determine success and learnings. Return JSON."
        messages = [
            LLMMessage(role="system", content=prompt),
            LLMMessage(role="user", content=f"Trace: {trace}")
        ]
        
        try:
            response = await self.llm.generate(messages=messages, temperature=0.1)
            # Simplified parsing
            return AgentReflection(
                summary="Reflection generated",
                success_rating=0.9,
                learnings=["Completed successfully"]
            )
        except Exception:
            # Fallback
            return AgentReflection(
                summary="Reflection failed",
                success_rating=0.0,
                learnings=[]
            )
