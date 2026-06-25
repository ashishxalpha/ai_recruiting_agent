from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from src.domain.enums import MemoryNamespace, MemoryRetentionPolicy

class MemorySource(BaseModel):
    source_id: UUID
    source_type: str
    created_by: Optional[str] = None
    workflow_id: Optional[UUID] = None
    model_name: Optional[str] = None
    prompt_version: Optional[str] = None
    source_entity: Optional[str] = None
    source_version: Optional[str] = None

class MemoryEdge(BaseModel):
    source_node_id: UUID
    target_node_id: UUID
    relationship_type: str
    weight: float = 1.0

class MemoryNode(BaseModel):
    node_id: UUID = Field(default_factory=uuid4)
    entity_type: str
    edges: List[MemoryEdge] = Field(default_factory=list)

class BaseMemory(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    namespace: MemoryNamespace
    importance: float = 0.5
    confidence: float = 0.5
    access_count: int = 0
    decay_score: float = 0.0
    retention_policy: MemoryRetentionPolicy
    external_reference: Optional[str] = None
    source: MemorySource
    node: Optional[MemoryNode] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)

class SemanticMemory(BaseMemory):
    content: str
    summary: Optional[str] = None
    embedding_id: Optional[str] = None

class EpisodicMemory(BaseMemory):
    event_description: str
    context: Dict[str, Any] = Field(default_factory=dict)

class ProceduralMemory(BaseMemory):
    procedure_name: str
    steps: List[str]

class WorkingMemory(BaseMemory):
    session_id: UUID
    volatile_state: Dict[str, Any] = Field(default_factory=dict)
