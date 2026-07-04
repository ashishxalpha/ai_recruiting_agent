from typing import List, Dict, Any
from src.application.tools.interfaces import ToolProvider, ToolExecutionContext
from src.domain.tool_models import ToolMetadata, ToolExecutionResult
from src.infrastructure.tools.mcp.transports import MCPTransport

class MCPProvider(ToolProvider):
    def __init__(self, provider_id: str, transport: MCPTransport):
        self._provider_id = provider_id
        self.transport = transport
        self.connected = False

    @property
    def provider_id(self) -> str:
        return self._provider_id

    async def connect(self) -> None:
        await self.transport.connect()
        self.connected = True
        
    async def disconnect(self) -> None:
        await self.transport.disconnect()
        self.connected = False

    async def health(self) -> str:
        if not self.connected:
            return "DISCONNECTED"
        try:
            # We could do a ping via transport, but for now just return CONNECTED
            return "CONNECTED"
        except Exception:
            return "UNHEALTHY"

    async def discover_tools(self) -> List[ToolMetadata]:
        # MCP specification defines a `tools/list` endpoint
        response = await self.transport.send_request("tools/list", {})
        
        # Stub parsing of response to ToolMetadata
        return []

    async def execute(self, tool_id: str, arguments: Dict[str, Any], context: ToolExecutionContext) -> ToolExecutionResult:
        # MCP specification defines a `tools/call` endpoint
        response = await self.transport.send_request("tools/call", {
            "name": tool_id,
            "arguments": arguments
        })
        
        return ToolExecutionResult(
            success=True,
            result=response,
            artifacts=[],
            execution_time=0.0,
            provider=self._provider_id,
            tool_name=tool_id
        )
