from pydantic import BaseModel, Field
from typing import Optional, Any, Generic, TypeVar, List, Dict
from datetime import datetime
from uuid import UUID

T = TypeVar("T")

class MemoryResponseDTO(BaseModel, Generic[T]):
    """Standard envelope for Memory Explorer API responses."""
    status: str  # "available", "not_available", "loading", "error", "no_data"
    reason: Optional[str] = None
    data: Optional[T] = None

class MemorySummaryDTO(BaseModel):
    id: UUID
    namespace: str
    memory_type: str
    content_snippet: str
    importance: float
    confidence: float
    created_at: datetime
    last_accessed_at: datetime

class MemoryListDTO(BaseModel):
    memories: List[MemorySummaryDTO]
    total_count: int

class MemoryDetailsDTO(BaseModel):
    id: UUID
    namespace: str
    memory_type: str
    content: str
    metadata: Dict[str, Any]
    importance: float
    confidence: float
    created_at: datetime
    updated_at: datetime
    last_accessed_at: datetime
    source_id: Optional[UUID] = None

# Retrieval Debugger Models
class MemoryRetrievalCandidateDTO(BaseModel):
    memory_id: UUID
    content_snippet: str
    similarity_score: float
    reranking_score: float
    importance: float
    recency: float
    decay: float
    confidence: float
    final_ranking: int
    inclusion_reason: Optional[str] = None
    exclusion_reason: Optional[str] = None

class MemoryRetrievalDTO(BaseModel):
    query: str
    namespace: Optional[str] = None
    retrieval_policy: str
    embedding_model: str
    execution_time_ms: float
    candidates: List[MemoryRetrievalCandidateDTO]

# Graph Topology for React Flow
class MemoryGraphNodeDTO(BaseModel):
    id: str
    type: str # 'memoryNode'
    data: Dict[str, Any] # Contains snippet, importance, confidence, namespace
    position: Dict[str, float]

class MemoryGraphEdgeDTO(BaseModel):
    id: str
    source: str
    target: str
    label: str # Relationship type (derived_from, references, duplicates, parent, child)
    type: Optional[str] = "smoothstep"
    data: Dict[str, Any] = Field(default_factory=dict) # strength, etc.

class MemoryGraphDTO(BaseModel):
    nodes: List[MemoryGraphNodeDTO]
    edges: List[MemoryGraphEdgeDTO]

class MemoryTimelineEntryDTO(BaseModel):
    event_id: UUID
    memory_id: UUID
    timestamp: datetime
    event_type: str  # "Created", "Retrieved", "Updated", "Consolidated", "Merged", "Forgotten", "Expired", "Archived"
    actor: str
    workflow_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MemoryTimelineDTO(BaseModel):
    entries: List[MemoryTimelineEntryDTO]

class MemoryRelationshipDTO(BaseModel):
    source_id: UUID
    target_id: UUID
    relationship_type: str
    strength: float
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MemoryRelationshipListDTO(BaseModel):
    relationships: List[MemoryRelationshipDTO]

class MemoryConsolidationEventDTO(BaseModel):
    consolidation_id: UUID
    timestamp: datetime
    input_memory_ids: List[UUID]
    output_memory_id: Optional[UUID] = None
    summary_generated: Optional[str] = None
    deduplication_occurred: bool
    importance_change: float
    decay_update: float
    latency_ms: float

class MemoryConsolidationDTO(BaseModel):
    consolidations: List[MemoryConsolidationEventDTO]

class MemoryStatisticsDTO(BaseModel):
    total_memories: int
    namespaces: Dict[str, int]
    memory_types: Dict[str, int]
    average_importance: float
    average_confidence: float
    decay_distribution: Dict[str, float]
    total_retrievals: int
    average_retrieval_latency_ms: float
    consolidation_count: int
    relationship_count: int
