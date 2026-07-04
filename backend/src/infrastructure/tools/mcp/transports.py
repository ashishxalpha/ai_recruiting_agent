from typing import Protocol, Any, Dict, List
from src.domain.tool_models import ToolMetadata

class MCPTransport(Protocol):
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    async def send_request(self, method: str, params: Dict[str, Any]) -> Any: ...

class StdioTransport(MCPTransport):
    def __init__(self, command: str, args: List[str]):
        self.command = command
        self.args = args
        self.connected = False
        
    async def connect(self) -> None:
        # Stub: Spawn subprocess
        self.connected = True
        
    async def disconnect(self) -> None:
        self.connected = False
        
    async def send_request(self, method: str, params: Dict[str, Any]) -> Any:
        if not self.connected:
            raise RuntimeError("Transport not connected")
        # Stub: Send JSON-RPC over stdin/stdout
        return {"stubbed_response": True}

class SSETransport(MCPTransport):
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.connected = False
        
    async def connect(self) -> None:
        # Stub: Connect HTTP client for SSE
        self.connected = True
        
    async def disconnect(self) -> None:
        self.connected = False
        
    async def send_request(self, method: str, params: Dict[str, Any]) -> Any:
        if not self.connected:
            raise RuntimeError("Transport not connected")
        # Stub: Send HTTP POST
        return {"stubbed_response": True}

class WebSocketTransport(MCPTransport):
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self.connected = False
        
    async def connect(self) -> None:
        self.connected = True
        
    async def disconnect(self) -> None:
        self.connected = False
        
    async def send_request(self, method: str, params: Dict[str, Any]) -> Any:
        if not self.connected:
            raise RuntimeError("Transport not connected")
        return {"stubbed_response": True}
