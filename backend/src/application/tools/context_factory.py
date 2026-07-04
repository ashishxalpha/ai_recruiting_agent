from typing import Dict, Any, Optional
from uuid import UUID
import uuid

from src.application.tools.interfaces import ToolExecutionContext
from src.domain.tool_models import ExecutionBudget

class ExecutionContextFactory:
    def create_context(self, 
        workflow_id: Optional[UUID] = None, 
        agent_id: Optional[UUID] = None,
        coordination_session_id: Optional[UUID] = None,
        request_id: Optional[UUID] = None,
        overrides: Dict[str, Any] = None
    ) -> ToolExecutionContext:
        
        ctx = ToolExecutionContext(
            request_id=request_id or uuid.uuid4(),
            workflow_id=workflow_id or uuid.uuid4(),
            execution_id=uuid.uuid4(),
            memory_context={},
            user_context={},
            system_context={},
            permissions=[],
            configuration={},
            trace_context={
                "agent_id": str(agent_id) if agent_id else None,
                "coordination_session_id": str(coordination_session_id) if coordination_session_id else None,
            },
            budget=ExecutionBudget(max_tokens=4000, current_tokens=0, max_duration_ms=30000)
        )
        
        if overrides:
            for k, v in overrides.items():
                if hasattr(ctx, k):
                    setattr(ctx, k, v)
                    
        return ctx
