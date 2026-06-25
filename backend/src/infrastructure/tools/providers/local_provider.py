import time
from typing import List, Dict, Any, Callable
from src.application.tools.interfaces import ToolProvider, ToolExecutionContext
from src.domain.tool_models import ToolMetadata, ToolExecutionResult

class LocalToolProvider(ToolProvider):
    def __init__(self, provider_id: str):
        self._provider_id = provider_id
        self.registry: Dict[str, Callable] = {}

    @property
    def provider_id(self) -> str:
        return self._provider_id

    def register_function(self, name: str, func: Callable):
        self.registry[name] = func

    async def connect(self) -> None:
        pass

    async def discover_tools(self) -> List[ToolMetadata]:
        return []

    async def execute(self, tool_id: str, arguments: Dict[str, Any], context: ToolExecutionContext) -> ToolExecutionResult:
        start_time = time.time()
        if tool_id not in self.registry:
            return ToolExecutionResult(
                success=False,
                result=None,
                execution_time=time.time() - start_time,
                provider=self._provider_id,
                tool_name=tool_id,
                errors=[f"Function {tool_id} not found in local registry"]
            )
        
        try:
            func = self.registry[tool_id]
            # Assuming all functions are async for now
            res = await func(**arguments)
            return ToolExecutionResult(
                success=True,
                result=res,
                execution_time=time.time() - start_time,
                provider=self._provider_id,
                tool_name=tool_id
            )
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                result=None,
                execution_time=time.time() - start_time,
                provider=self._provider_id,
                tool_name=tool_id,
                errors=[str(e)]
            )

    async def health(self) -> str:
        return "healthy"

    async def disconnect(self) -> None:
        pass
