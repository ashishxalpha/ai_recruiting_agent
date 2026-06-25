from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class ToolCategory(str, Enum):
    FILESYSTEM = "FILESYSTEM"
    DATABASE = "DATABASE"
    DEVELOPMENT = "DEVELOPMENT"
    COMMUNICATION = "COMMUNICATION"
    SCHEDULING = "SCHEDULING"
    KNOWLEDGE = "KNOWLEDGE"
    PRODUCTIVITY = "PRODUCTIVITY"
    OTHER = "OTHER"

class ExecutionTarget(str, Enum):
    LOCAL = "LOCAL"
    REMOTE = "REMOTE"
    MCP = "MCP"
    FUTURE_CLUSTER = "FUTURE_CLUSTER"

class ToolContract(BaseModel):
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    examples: List[Dict[str, Any]] = Field(default_factory=list)
    version: str = "1.0.0"
    error_codes: Dict[str, str] = Field(default_factory=dict)

class ToolMetadata(ToolContract):
    tool_id: str
    name: str
    description: str
    provider: str
    capabilities: List[str]
    timeout: int = 30
    estimated_cost: float = 0.0
    permissions: List[str] = Field(default_factory=list)
    health_status: str = "healthy"
    rate_limits: Dict[str, Any] = Field(default_factory=dict)
    supported_operations: List[str] = Field(default_factory=list)
    execution_target: ExecutionTarget = ExecutionTarget.LOCAL
    approval_required: bool = False
    category: ToolCategory = ToolCategory.OTHER

class ExecutionBudget(BaseModel):
    max_cost: float = 0.0
    max_tokens: int = 0
    max_tool_calls: int = 0
    timeout: int = 30

class ToolSession(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    execution_id: UUID
    tools_used: List[str] = Field(default_factory=list)
    duration: float = 0.0
    total_cost: float = 0.0
    budget: Optional[ExecutionBudget] = None

class ToolExecutionResult(BaseModel):
    success: bool
    result: Any
    execution_time: float
    provider: str
    tool_name: str
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    cost: float = 0.0
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    logs: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    references: List[str] = Field(default_factory=list)
