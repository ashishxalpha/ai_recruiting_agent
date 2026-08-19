from pydantic import BaseModel

class DashboardSummaryDTO(BaseModel):
    total_candidates: int
    active_jobs: int
    active_workflows: int
    pending_feedback: int
    running_agents: int
    active_coordination_sessions: int
    memory_count: int
    todays_uploads: int

class DashboardActivityDTO(BaseModel):
    today: int
    week: int

class DashboardHealthStatusDTO(BaseModel):
    status: str
    message: str
    latency_ms: float

class DashboardHealthDTO(BaseModel):
    database: DashboardHealthStatusDTO
    redis: DashboardHealthStatusDTO
    workflow_engine: DashboardHealthStatusDTO
    agent_swarm: DashboardHealthStatusDTO
    memory_engine: DashboardHealthStatusDTO
    overall_status: str

class DashboardMetricsDTO(BaseModel):
    summary: DashboardSummaryDTO
    activity: DashboardActivityDTO
    health: DashboardHealthDTO

class RecentActivityDTO(BaseModel):
    activities: list
