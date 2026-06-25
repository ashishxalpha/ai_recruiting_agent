from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class SkillContract(BaseModel):
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    examples: List[Dict[str, Any]] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    required_memory: List[str] = Field(default_factory=list)
    version: str
    estimated_cost: float
    latency_estimate: float

class AgentSkill(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    contract: SkillContract
    health: str = "HEALTHY"

class OrganizationRole(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    assigned_skills: List[str] = Field(default_factory=list)

class OrganizationPolicy(BaseModel):
    approval_policies: Dict[str, Any] = Field(default_factory=dict)
    cost_limits: float = 50.0
    parallelism: int = 5
    memory_access: List[str] = Field(default_factory=list)
    tool_access: List[str] = Field(default_factory=list)
    human_approval: bool = False

class OrganizationConfiguration(BaseModel):
    enabled_roles: List[str] = Field(default_factory=list)
    enabled_skills: List[str] = Field(default_factory=list)
    planning_strategy: str = "DEFAULT"
    reflection_strategy: str = "DEFAULT"
    tool_strategy: str = "DEFAULT"
    memory_strategy: str = "DEFAULT"
    policies: OrganizationPolicy = Field(default_factory=OrganizationPolicy)
    execution_budgets: Dict[str, float] = Field(default_factory=dict)

class OrganizationHealth(BaseModel):
    role_availability: Dict[str, str] = Field(default_factory=dict)
    skill_failures: int = 0
    goal_throughput: float = 0.0
    latency: float = 0.0
    tool_cost: float = 0.0
    memory_usage: float = 0.0
    human_intervention: float = 0.0
    consensus_failures: int = 0

class OrganizationMetrics(BaseModel):
    goal_completion_rate: float = 0.0
    average_execution_latency: float = 0.0
    skill_utilization: Dict[str, int] = Field(default_factory=dict)
    role_utilization: Dict[str, int] = Field(default_factory=dict)
    cost_per_workflow: float = 0.0
    health: OrganizationHealth = Field(default_factory=OrganizationHealth)

class GoalTemplate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    workflow_structure: Dict[str, Any]

class OrganizationGoal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    template_id: Optional[UUID] = None
    status: str = "PENDING"

class SkillDependencyGraph(BaseModel):
    graph_id: UUID = Field(default_factory=uuid4)
    goal_id: UUID
    execution_order: List[Dict[str, Any]] = Field(default_factory=list)

class OrganizationPlugin(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    config: OrganizationConfiguration

class RecruitingOrganization(OrganizationPlugin):
    name: str = "RecruitingOrganization"
