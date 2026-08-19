import time
from typing import List, Dict, Any
from src.application.tools.interfaces import ToolProvider, ToolExecutionContext
from src.domain.tool_models import ToolMetadata, ToolExecutionResult

class MCPToolProvider(ToolProvider):
    def __init__(self, provider_id: str, transport_type: str = "stdio", command: str = None, args: List[str] = None):
        self._provider_id = provider_id
        self.transport_type = transport_type
        self.command = command
        self.args = args or []
        self._connected = False

    @property
    def provider_id(self) -> str:
        return self._provider_id

    async def connect(self) -> None:
        # Utilizing official python `mcp` SDK to spawn stdio/SSE server would go here
        self._connected = True

    async def discover_tools(self) -> List[ToolMetadata]:
        if not self._connected:
            await self.connect()
        return []

    async def execute(self, tool_id: str, arguments: Dict[str, Any], context: ToolExecutionContext) -> ToolExecutionResult:
        start_time = time.time()
        
        if self.transport_type == "stdio" and self.command:
            import asyncio
            import json
            
            try:
                process = await asyncio.create_subprocess_exec(
                    self.command, *self.args,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "execute_tool",
                    "params": {
                        "tool_id": tool_id,
                        "arguments": arguments,
                        "context": context.model_dump(mode="json") if hasattr(context, "model_dump") else str(context)
                    }
                }
                
                stdout, stderr = await process.communicate(input=json.dumps(request).encode() + b"\n")
                
                if process.returncode != 0:
                    raise Exception(f"MCP Process Failed: {stderr.decode()}")
                    
                try:
                    response = json.loads(stdout.decode())
                    result_data = response.get("result", stdout.decode())
                except:
                    result_data = stdout.decode()
                
                return ToolExecutionResult(
                    success=True,
                    result=result_data if isinstance(result_data, dict) else {"output": result_data},
                    execution_time=time.time() - start_time,
                    provider=self._provider_id,
                    tool_name=tool_id
                )
            except Exception as e:
                return ToolExecutionResult(
                    success=False,
                    result={"error": str(e)},
                    execution_time=time.time() - start_time,
                    provider=self._provider_id,
                    tool_name=tool_id
                )
        else:
            raise NotImplementedError(f"Transport type {self.transport_type} is not fully implemented.")

    async def health(self) -> str:
        return "healthy" if self._connected else "offline"

    async def disconnect(self) -> None:
        self._connected = False
