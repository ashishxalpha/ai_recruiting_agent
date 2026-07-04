from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar, List

T = TypeVar("T")

class AnalyticsResponseDTO(BaseModel, Generic[T]):
    status: str  # "available", "not_available", "loading", "error"
    reason: Optional[str] = None
    data: Optional[T] = None

class RecruitingFunnelDTO(BaseModel):
    applications: int
    processing: int
    review: int
    shortlisted: int
    interview: int
    offer: int
    hired: int

class MatchingAnalyticsDTO(BaseModel):
    average_match_score: float
    average_confidence: float
    precision: float
    recall: float
    ndcg: float
    approval_rate: float
    recruiter_agreement: float
    hire_conversion: float

class WorkflowAnalyticsDTO(BaseModel):
    average_duration_ms: float
    success_rate: float
    retry_count: int
    paused_workflows: int
    failed_workflows: int
    human_approvals: int
    checkpoint_recovery: int

class MemoryAnalyticsDTO(BaseModel):
    memory_count: int
    memory_types: dict[str, int]
    retrieval_latency_ms: float
    average_importance: float
    decay_distribution: dict[str, int]
    consolidation_metrics: dict[str, Any]

class AgentAnalyticsDTO(BaseModel):
    running_agents: int
    completed_sessions: int
    iterations: int
    thoughts: int
    actions: int
    reflections: int
    replay_count: int

class ToolAnalyticsDTO(BaseModel):
    executions: int
    latency_ms: float
    failures: int
    provider_health: dict[str, str]
    cache_hit_rate: float
    cost_usd: float

class OrganizationAnalyticsDTO(BaseModel):
    goals_active: int
    executions: int
    role_utilization: dict[str, float]
    skill_usage: dict[str, int]
    learning_loop_metrics: dict[str, Any]
    policy_violations: int

class HealthComponentDTO(BaseModel):
    status: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None

class PlatformHealthDTO(BaseModel):
    database: HealthComponentDTO
    workflow_engine: HealthComponentDTO
    memory_engine: HealthComponentDTO
    agent_runtime: HealthComponentDTO
    coordination_platform: HealthComponentDTO
    tool_platform: HealthComponentDTO
    sse: HealthComponentDTO
    opentelemetry: HealthComponentDTO
