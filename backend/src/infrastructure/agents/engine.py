from uuid import UUID
from typing import Dict, Any
from src.application.agents.interfaces import AgentRuntime, CognitivePipeline, AgentExecutor, AgentSession
from src.domain.agent_models import Agent, AgentContext, ReasoningTrace, AgentLifecycle, StepType
import os
import json
import uuid
import datetime

class DefaultAgentRuntime(AgentRuntime):
    def __init__(self, pipeline: CognitivePipeline):
        self.pipeline = pipeline

    async def create(self, template_id: UUID) -> Agent:
        return Agent(name="RuntimeAgent", template_id=template_id)

    async def start(self, agent_id: UUID, context: AgentContext) -> AgentSession:
        session = AgentSession(agent_id=agent_id, workflow_id=UUID("00000000-0000-0000-0000-000000000000"), status=AgentLifecycle.RUNNING)
        # Mocking an iteration
        await self.pipeline.execute_iteration(session, context)
        return session

    async def pause(self, agent_id: UUID) -> None:
        pass

    async def resume(self, agent_id: UUID) -> None:
        pass

    async def cancel(self, agent_id: UUID) -> None:
        pass

    async def terminate(self, agent_id: UUID) -> None:
        pass

    async def heartbeat(self, agent_id: UUID) -> None:
        pass

    async def status(self, agent_id: UUID) -> str:
        return AgentLifecycle.RUNNING

class DefaultCognitivePipeline(CognitivePipeline):
    async def execute_iteration(self, session: AgentSession, context: AgentContext) -> ReasoningTrace:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment.")
            
        import httpx
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = "You are an autonomous recruiting agent. Based on the user context, decide the next action."
        user_prompt = f"Goal: {context.goal}\nMemory: {context.memory}\nAvailable Tools: {context.tools}"
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 500
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
        content = data["choices"][0]["message"]["content"]
        
        return ReasoningTrace(
            id=uuid.uuid4(),
            session_id=session.agent_id,
            step_type=StepType.THOUGHT,
            content=content,
            created_at=datetime.datetime.utcnow()
        )

class DefaultAgentExecutor(AgentExecutor):
    async def execute_action(self, action: Any, context: AgentContext) -> Dict[str, Any]:
        return {"result": "success"}
