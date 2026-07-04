import asyncio
import uuid
import time
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool

from src.application.tools.interfaces import ToolProvider, ToolExecutionContext
from src.domain.tool_models import ToolMetadata, ToolExecutionResult, ExecutionBudget
from src.infrastructure.tools.provider_manager import InMemoryProviderManager
from src.application.tools.capability_resolver import DefaultCapabilityResolver
from src.infrastructure.tools.circuit_breaker import CircuitBreakerManager, CircuitState
from src.infrastructure.tools.cache import InMemoryToolCache
from src.infrastructure.tools.pipeline import ToolExecutionPipeline, ToolExecutionCompleted
from src.infrastructure.tools.execution_recorder import ExecutionRecorder
from src.infrastructure.events.event_bus import EventBus
from src.application.tools.context_factory import ExecutionContextFactory
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://copilot:copilot_password@localhost:5432/ai_recruiting")

# Mocks
class MockRegistry:
    async def discover(self):
        return [
            ToolMetadata(
                tool_id="read_file", name="read_file", description="mock_fs", provider="mock_fs", capabilities=["filesystem"],
                input_schema={}, output_schema={}
            ),
            ToolMetadata(
                tool_id="fallback_read_file", name="fallback_read_file", description="fallback_fs", provider="fallback_fs", capabilities=["filesystem"],
                input_schema={}, output_schema={}
            )
        ]

class MockProvider(ToolProvider):
    def __init__(self, provider_id: str, fail_count: int = 0):
        self._provider_id = provider_id
        self.fail_count = fail_count
        self.calls = 0

    @property
    def provider_id(self) -> str: return self._provider_id
    
    async def connect(self): pass
    async def disconnect(self): pass
    async def discover_tools(self): return []
    async def health(self): return "CONNECTED"
    
    async def execute(self, tool_id, args, context):
        self.calls += 1
        if self.calls <= self.fail_count:
            raise RuntimeError("Simulated provider failure")
        return ToolExecutionResult(
            success=True, result={"result": f"Executed by {self._provider_id}"}, artifacts=[],
            execution_time=0.1, provider=self._provider_id, tool_name=tool_id
        )


class FailoverCapabilityResolver(DefaultCapabilityResolver):
    async def resolve(self, capability: str, operation: str, fallback: bool = False):
        tools = await self.registry.discover()
        for tool in tools:
            # Simple failover simulation based on fallback flag
            if fallback and "fallback" in tool.name and (operation in tool.name or tool.name == operation):
                return type("ResolvedCapability", (), {"provider_id": tool.provider, "tool_id": tool.name, "operation": operation})()
            elif not fallback and "fallback" not in tool.name and (operation in tool.name or tool.name == operation):
                return type("ResolvedCapability", (), {"provider_id": tool.provider, "tool_id": tool.name, "operation": operation})()
        raise ValueError("Cannot resolve")


async def test_circuit_breaker_recovery():
    print("--- Test Circuit Breaker Recovery ---")
    cb_manager = CircuitBreakerManager(default_threshold=2, default_cooldown=1) # 1 sec cooldown
    breaker = cb_manager.get_breaker("test_provider")
    
    assert breaker.state == CircuitState.CLOSED
    
    # Fail twice
    breaker.record_failure()
    breaker.record_failure()
    
    assert breaker.state == CircuitState.OPEN
    assert not breaker.allow_request()
    
    # Wait for cooldown
    print("Waiting for cooldown...")
    time.sleep(1.1)
    
    assert breaker.allow_request()
    assert breaker.state == CircuitState.HALF_OPEN
    
    # Success resets it
    breaker.record_success()
    assert breaker.state == CircuitState.CLOSED
    print("Circuit Breaker Recovery passed!")

async def test_end_to_end_pipeline():
    print("\n--- Test E2E Pipeline with Execution Recorder ---")
    
    engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
    AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    
    recorder = ExecutionRecorder(AsyncSessionLocal)
    recorder.start()
    
    # Setup Pipeline
    registry = MockRegistry()
    resolver = DefaultCapabilityResolver(registry)
    
    provider_manager = InMemoryProviderManager()
    await provider_manager.register_provider(MockProvider("mock_fs"))
    
    breaker_manager = CircuitBreakerManager()
    cache = InMemoryToolCache()
    
    pipeline = ToolExecutionPipeline(resolver, provider_manager, breaker_manager, cache)
    context_factory = ExecutionContextFactory()
    
    context = context_factory.create_context(workflow_id=uuid.uuid4())
    
    # Execute
    print("Executing capability 'filesystem' operation 'read_file'...")
    result = await pipeline.execute("filesystem", "read_file", {"path": "/test"}, context)
    
    assert result.success
    assert result.result["result"] == "Executed by mock_fs"
    
    # Wait for async event to be processed
    await asyncio.sleep(0.5)
    
    # Verify DB record
    async with AsyncSessionLocal() as session:
        res = await session.execute(text(f"SELECT status, provider, tool FROM tool_executions WHERE id = '{context.execution_id}'"))
        record = res.fetchone()
        assert record is not None
        print(f"Tool Execution Record found: {record}")
        assert record[0] == "SUCCESS"
        assert record[1] == "mock_fs"
        assert record[2] == "read_file"
        
    print("E2E Pipeline passed!")

if __name__ == "__main__":
    asyncio.run(test_circuit_breaker_recovery())
    asyncio.run(test_end_to_end_pipeline())
