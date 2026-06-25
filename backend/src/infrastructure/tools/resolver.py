from src.application.tools.interfaces import CapabilityResolver, ToolRegistry
from src.domain.tool_models import ToolMetadata

class DefaultCapabilityResolver(CapabilityResolver):
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def resolve(self, capability: str, operation: str) -> ToolMetadata:
        # Mock logic to find the first tool that provides this capability and operation
        tools = await self.registry.discover()
        for t in tools:
            if capability in t.capabilities and operation in t.supported_operations:
                return t
        return None
