import uuid
from typing import Dict, Any
from uuid import UUID
from src.application.tools.interfaces import ContextBuilder, ToolExecutionContext
from src.domain.tool_models import ExecutionBudget

class DefaultContextBuilder(ContextBuilder):
    async def build(self, workflow_id: UUID, overrides: Dict[str, Any] = None) -> ToolExecutionContext:
        overrides = overrides or {}
        
        # In a real system, we'd fetch actual memory/user/system context from the DB
        return ToolExecutionContext(
            request_id=uuid.uuid4(),
            workflow_id=workflow_id,
            execution_id=uuid.uuid4(),
            memory_context={"mock": "memory"},
            user_context={"mock": "user"},
            system_context={"mock": "system"},
            permissions=["filesystem.read", "filesystem.write"],
            budget=ExecutionBudget(max_cost=1.0, max_tokens=10000, max_tool_calls=5, timeout=60),
            **overrides
        )
