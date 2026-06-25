from typing import Protocol, List, Optional, Any, Dict
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from src.domain.memory_models import BaseMemory
from src.domain.interfaces.memory_repository import MemoryRepository

class RetrievalPolicy(Protocol):
    """Abstraction defining how memories should be ranked/filtered."""
    def apply(self, query: str, memories: List[BaseMemory]) -> List[BaseMemory]:
        ...

class SemanticRetrievalPolicy(RetrievalPolicy):
    def apply(self, query: str, memories: List[BaseMemory]) -> List[BaseMemory]:
        # Would re-rank based purely on vector cosine similarity
        return memories

class RecencyRetrievalPolicy(RetrievalPolicy):
    def apply(self, query: str, memories: List[BaseMemory]) -> List[BaseMemory]:
        # Re-rank based on created_at and last_accessed
        return memories

class HybridRetrievalPolicy(RetrievalPolicy):
    def __init__(self, w_sim=0.4, w_rec=0.2, w_imp=0.2, w_conf=0.1, w_dec=0.1):
        self.weights = {"sim": w_sim, "rec": w_rec, "imp": w_imp, "conf": w_conf, "dec": w_dec}
        
    def apply(self, query: str, memories: List[BaseMemory]) -> List[BaseMemory]:
        # Implement dynamic scoring
        return memories

class MemoryContext(BaseModel):
    retrieved_memories: List[BaseMemory]
    retrieval_strategy: str
    retrieval_reason: str
    confidence: float
    search_statistics: Dict[str, Any]
    warnings: List[str] = Field(default_factory=list)
    missing_context: List[str] = Field(default_factory=list)

class MemoryEngine(Protocol):
    async def store(self, memory: BaseMemory) -> BaseMemory:
        ...
        
    async def retrieve(self, query: str, policy: RetrievalPolicy, filters: Dict[str, Any] = None) -> MemoryContext:
        ...
        
    async def update(self, memory: BaseMemory) -> BaseMemory:
        ...
        
    async def delete(self, memory_id: UUID) -> None:
        ...
        
    async def consolidate(self) -> None:
        ...

class HybridMemoryEngine(MemoryEngine):
    def __init__(self, repo: MemoryRepository):
        self.repo = repo

    async def store(self, memory: BaseMemory) -> BaseMemory:
        saved = await self.repo.save(memory)
        # Emit MemoryCreated event here to trigger background embedding job
        return saved

    async def retrieve(self, query: str, policy: RetrievalPolicy, filters: Dict[str, Any] = None) -> MemoryContext:
        raw_memories = await self.repo.search(query, filters or {}, limit=100)
        ranked_memories = policy.apply(query, raw_memories)
        
        return MemoryContext(
            retrieved_memories=ranked_memories[:10],
            retrieval_strategy=policy.__class__.__name__,
            retrieval_reason="Orchestrator context resolution",
            confidence=0.85,
            search_statistics={"total_hits": len(raw_memories), "latency_ms": 45}
        )

    async def update(self, memory: BaseMemory) -> BaseMemory:
        return await self.repo.save(memory)

    async def delete(self, memory_id: UUID) -> None:
        await self.repo.delete(memory_id)

    async def consolidate(self) -> None:
        pass
