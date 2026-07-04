from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DashboardSummaryDTO(BaseModel):
    candidates: int = 0
    jobs: int = 0
    workflows: int = 0
    pending_feedback: int = 0
    running_agents: int = 0
    active_coordination_sessions: int = 0
    memory_count: int = 0
    todays_uploads: int = 0

class DashboardActivityDTO(BaseModel):
    today: int
    week: int

class DashboardHealthStatusDTO(BaseModel):
    status: str
    message: Optional[str] = None
    latency_ms: Optional[float] = None

class DashboardHealthDTO(BaseModel):
    agents: str
    tools: str

class DashboardMetricsDTO(BaseModel):
    summary: DashboardSummaryDTO
    activity: DashboardActivityDTO
    health: DashboardHealthDTO

class RecentActivityEntryDTO(BaseModel):
    event_id: str
    timestamp: datetime
    source: str # e.g. "workflow", "agent", "memory", "coordination"
    description: str
    metadata: dict

class RecentActivityDTO(BaseModel):
    activities: List[RecentActivityEntryDTO]
