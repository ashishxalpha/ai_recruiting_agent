from typing import Dict, Any, Optional
import time
import uuid
import datetime

from src.application.tools.interfaces import (
    ToolExecutionContext, CapabilityResolver, ProviderManager, ToolCache, ToolProvider
)
from src.domain.tool_models import ToolExecutionResult
from src.infrastructure.tools.circuit_breaker import CircuitBreakerManager, CircuitState
from src.infrastructure.events.event_bus import EventBus
from pydantic import BaseModel

class ToolExecutionCompleted(BaseModel):
    event_id: uuid.UUID
    occurred_at: datetime.datetime
    execution_id: uuid.UUID
    workflow_id: Optional[uuid.UUID]
    agent_id: Optional[uuid.UUID]
    trace_id: Optional[str]
    provider_id: str
    tool_id: str
    operation: str
    latency_ms: float
    status: str
    error: Optional[str] = None
    retry_count: int = 0
    # Omitting full arguments/artifacts for brevity in event schema if they can be large, 
    # but we can include a summary or reference.
    result_summary: Optional[str] = None

class ToolExecutionPipeline:
    def __init__(self,
                 resolver: CapabilityResolver,
                 provider_manager: ProviderManager,
                 breaker_manager: CircuitBreakerManager,
                 cache: ToolCache):
        self.resolver = resolver
        self.provider_manager = provider_manager
        self.breaker_manager = breaker_manager
        self.cache = cache

    async def execute(self, capability: str, operation: str, arguments: Dict[str, Any], context: ToolExecutionContext) -> ToolExecutionResult:
        start_time = time.time()
        
        # 1. Permission (Stubbed for Phase 3)
        # Check context.permissions
        
        # 2. Budget (Stubbed for Phase 3)
        # if context.budget.current_tokens > context.budget.max_tokens: raise ...

        # 3. Provider Resolution
        resolved = await self.resolver.resolve(capability, operation)
        
        # 4. Circuit Breaker
        breaker = self.breaker_manager.get_breaker(resolved.provider_id)
        if not breaker.allow_request():
            raise RuntimeError(f"Circuit breaker for provider {resolved.provider_id} is OPEN. Request rejected.")
            
        provider = await self.provider_manager.get_provider(resolved.provider_id)
        
        # Cache Check (Stubbed/Passthrough logic for cache layer here)
        cache_key = f"{resolved.provider_id}:{resolved.tool_id}:{operation}:{hash(frozenset(arguments.items()))}"
        cached_result = await self.cache.retrieve(cache_key)
        if cached_result:
            return cached_result
            
        retry_count = 0
        max_retries = 3 # Can be pulled from context or tool policy
        
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                retry_count = attempt
                
                # 5. Execution
                result = await provider.execute(resolved.tool_id, arguments, context)
                
                breaker.record_success()
                
                # Cache Save
                await self.cache.cache(cache_key, result, ttl=60)
                
                # Telemetry Event
                self._emit_completion(context, resolved, start_time, "SUCCESS", retry_count, result)
                
                return result
                
            except Exception as e:
                breaker.record_failure()
                last_exception = e
                
                if not breaker.allow_request():
                    # Circuit opened during retries
                    break
                    
                # Simple backoff stub
                await __import__('asyncio').sleep(0.5 * (attempt + 1))
                
        # Telemetry Failure Event
        self._emit_completion(context, resolved, start_time, "FAILED", retry_count, error=str(last_exception))
        
        raise last_exception
        
    def _emit_completion(self, context, resolved, start_time, status, retry_count, result: Optional[ToolExecutionResult] = None, error: str = None):
        latency = (time.time() - start_time) * 1000
        
        event = ToolExecutionCompleted(
            event_id=uuid.uuid4(),
            occurred_at=datetime.datetime.utcnow(),
            execution_id=context.execution_id,
            workflow_id=context.workflow_id,
            agent_id=uuid.UUID(context.trace_context.get("agent_id")) if context.trace_context.get("agent_id") else None,
            trace_id=context.trace_context.get("trace_id", str(uuid.uuid4())),
            provider_id=resolved.provider_id,
            tool_id=resolved.tool_id,
            operation=resolved.operation,
            latency_ms=latency,
            status=status,
            error=error,
            retry_count=retry_count,
            result_summary="Success" if result else None
        )
        
        EventBus.publish(event)
