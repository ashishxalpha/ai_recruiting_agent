from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid

class AgentBudget(BaseModel):
    max_iterations: int = 10
    max_tokens: int = 50000
    max_cost: float = 2.0
    max_runtime_sec: int = 300
    max_tool_calls: int = 20
    
    current_iterations: int = 0
    current_tokens: int = 0
    current_cost: float = 0.0
    current_runtime_sec: int = 0
    current_tool_calls: int = 0

    def check_limits(self):
        if self.current_iterations >= self.max_iterations:
            raise RuntimeError(f"Budget exceeded: max iterations ({self.max_iterations}) reached")
        if self.current_tokens >= self.max_tokens:
            raise RuntimeError(f"Budget exceeded: max tokens ({self.max_tokens}) reached")
        if self.current_cost >= self.max_cost:
            raise RuntimeError(f"Budget exceeded: max cost ({self.max_cost}) reached")
        if self.current_runtime_sec >= self.max_runtime_sec:
            raise RuntimeError(f"Budget exceeded: max runtime ({self.max_runtime_sec}s) reached")
        if self.current_tool_calls >= self.max_tool_calls:
            raise RuntimeError(f"Budget exceeded: max tool calls ({self.max_tool_calls}) reached")

class TraceContext(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class AgentExecutionContext(BaseModel):
    agent_id: uuid.UUID
    session_id: uuid.UUID
    workflow_id: Optional[uuid.UUID] = None
    organization_id: Optional[uuid.UUID] = None
    
    memory_context: Dict[str, Any] = Field(default_factory=dict)
    policies: Dict[str, Any] = Field(default_factory=dict)
    tool_context: Dict[str, Any] = Field(default_factory=dict)
    
    budget: AgentBudget = Field(default_factory=AgentBudget)
    trace: TraceContext = Field(default_factory=TraceContext)
    
    # Injected references to engines/providers (not serialized)
    # Passed dynamically during runtime if needed, though typically we pass context TO the services
    
    class Config:
        arbitrary_types_allowed = True
