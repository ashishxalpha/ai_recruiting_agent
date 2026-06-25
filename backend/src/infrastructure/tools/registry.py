from typing import List
from src.application.tools.interfaces import ToolRegistry
from src.domain.tool_models import ToolMetadata

class InMemoryToolRegistry(ToolRegistry):
    def __init__(self):
        self._tools = {}

    async def register(self, metadata: ToolMetadata) -> None:
        self._tools[metadata.tool_id] = metadata

    async def unregister(self, tool_id: str) -> None:
        if tool_id in self._tools:
            del self._tools[tool_id]

    async def discover(self) -> List[ToolMetadata]:
        return list(self._tools.values())

    async def search(self, query: str) -> List[ToolMetadata]:
        return [t for t in self._tools.values() if query.lower() in t.name.lower() or query.lower() in t.description.lower()]

    async def get(self, tool_id: str) -> ToolMetadata:
        return self._tools.get(tool_id)

    async def list(self) -> List[ToolMetadata]:
        return list(self._tools.values())
