from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class AgentRuntimeDTO(BaseModel):
    id: str
    status: str
    current_task: str | None
    uptime: int

class AgentSessionDTO(BaseModel):
    session_id: str
    started_at: datetime
    duration: int

class AgentThoughtDTO(BaseModel):
    thought_id: str
    timestamp: datetime
    content: str
    confidence: float

class AgentActionDTO(BaseModel):
    action_id: str
    timestamp: datetime
    tool_name: str
    input: Dict[str, Any]
    result: str

class AgentToolDTO(BaseModel):
    tool_name: str
    description: str
    usage_count: int

class AgentMemoryDTO(BaseModel):
    memory_id: str
    content: str
    relevance: float

class AgentReflectionDTO(BaseModel):
    reflection_id: str
    timestamp: datetime
    insight: str

class AgentReplayDTO(BaseModel):
    events: List[Dict[str, Any]]
