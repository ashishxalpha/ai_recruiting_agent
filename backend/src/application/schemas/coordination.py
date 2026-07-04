from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class CoordinationSessionDTO(BaseModel):
    session_id: str
    status: str
    active_agents: int
    started_at: datetime

class CoordinationConsensusDTO(BaseModel):
    decision_id: str
    topic: str
    resolution: str
    agents_involved: List[str]

class CoordinationHandoffDTO(BaseModel):
    handoff_id: str
    from_agent: str
    to_agent: str
    reason: str
    timestamp: datetime

class CoordinationConflictDTO(BaseModel):
    conflict_id: str
    issue: str
    status: str
    resolved_by: str | None
