from typing import Optional, Dict
from src.application.tools.interfaces import ToolCache
from src.domain.tool_models import ToolExecutionResult
import time

class InMemoryToolCache(ToolCache):
    def __init__(self):
        self._cache: Dict[str, dict] = {}

    async def cache(self, key: str, result: ToolExecutionResult, ttl: int) -> None:
        self._cache[key] = {
            "result": result,
            "expires_at": time.time() + ttl
        }

    async def retrieve(self, key: str) -> Optional[ToolExecutionResult]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires_at"]:
                return entry["result"]
            else:
                del self._cache[key]
        return None

    async def invalidate(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    async def invalidate_by_provider(self, provider_id: str) -> None:
        keys_to_delete = [k for k in self._cache.keys() if k.startswith(f"{provider_id}:")]
        for k in keys_to_delete:
            del self._cache[k]

    async def invalidate_by_capability(self, capability: str) -> None:
        # Complex to do accurately without index, but stubbing for Phase 3
        pass
