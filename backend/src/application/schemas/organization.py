from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrganizationGoalDTO(BaseModel):
    id: str
    title: str
    description: str
    status: str
    target_date: datetime

class OrganizationRoleDTO(BaseModel):
    id: str
    title: str
    department: str
    headcount: int

class OrganizationSkillDTO(BaseModel):
    id: str
    name: str
    category: str
    demand_score: float

class OrganizationExecutionDTO(BaseModel):
    execution_id: str
    agent_id: str
    status: str
    started_at: datetime
    completed_at: datetime | None

class OrganizationPolicyDTO(BaseModel):
    id: str
    name: str
    description: str
    enforced: bool

class OrganizationLearningDTO(BaseModel):
    id: str
    topic: str
    insight: str
    confidence: float
    discovered_at: datetime

class OrganizationMetricDTO(BaseModel):
    metric_name: str
    value: float
    trend: str # 'up', 'down', 'stable'

class OrganizationActivityDTO(BaseModel):
    event_id: str
    timestamp: datetime
    actor: str
    action: str
    target: str
