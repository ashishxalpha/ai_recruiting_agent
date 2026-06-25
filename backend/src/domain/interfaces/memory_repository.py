from typing import Protocol, List, Optional, Any, Dict
from uuid import UUID
from src.domain.memory_models import BaseMemory, WorkingMemory
from src.domain.knowledge_models import KnowledgeRecord

class MemoryRepository(Protocol):
    async def save(self, memory: BaseMemory) -> BaseMemory:
        ...
        
    async def get(self, memory_id: UUID) -> Optional[BaseMemory]:
        ...
        
    async def delete(self, memory_id: UUID) -> None:
        ...
        
    async def search(self, query: str, filters: Dict[str, Any], limit: int) -> List[BaseMemory]:
        ...

class WorkingMemoryStore(Protocol):
    async def set_state(self, session_id: UUID, state: WorkingMemory) -> None:
        ...
        
    async def get_state(self, session_id: UUID) -> Optional[WorkingMemory]:
        ...
        
    async def clear_state(self, session_id: UUID) -> None:
        ...

class KnowledgeRepository(Protocol):
    """Stub for future knowledge graph expansions"""
    async def save(self, record: KnowledgeRecord) -> KnowledgeRecord:
        ...
