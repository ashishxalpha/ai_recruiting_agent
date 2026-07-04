from src.application.tools.interfaces import CapabilityResolver, ResolvedCapability, ToolRegistry

class DefaultCapabilityResolver(CapabilityResolver):
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def resolve(self, capability: str, operation: str) -> ResolvedCapability:
        """
        Resolves Capability -> Provider -> Tool -> Operation.
        For example:
        capability: "filesystem"
        operation: "read_file"
        Returns a ResolvedCapability with provider, tool_id, and operation.
        """
        tools = await self.registry.discover()
        
        for tool in tools:
            # We assume tool metadata includes a capability tag or namespace
            # For simplicity, if the tool name matches the capability or capability is in its tags
            # and the operation is supported (or if the tool *is* the operation)
            
            # Simple heuristic: capability maps to tool group/provider, operation maps to specific tool
            # In MCP, a provider exposes multiple tools.
            # E.g., capability "filesystem", operation "read_file" -> tool_id="read_file"
            
            if tool.name == operation or operation in tool.name:
                # In a robust implementation, we'd check if the tool is part of the requested capability namespace
                return ResolvedCapability(
                    provider_id=tool.provider,
                    tool_id=tool.name,
                    operation=operation
                )
                
        raise ValueError(f"Could not resolve capability '{capability}' with operation '{operation}'")
