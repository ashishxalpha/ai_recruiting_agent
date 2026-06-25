import time
from typing import Dict, Any
from uuid import UUID
from src.application.tools.interfaces import ToolExecutor, ToolExecutionContext, CapabilityResolver, ProviderManager, ToolPolicy
from src.domain.tool_models import ToolExecutionResult

class SecureToolExecutor(ToolExecutor):
    def __init__(self, resolver: CapabilityResolver, provider_manager: ProviderManager, policy: ToolPolicy):
        self.resolver = resolver
        self.provider_manager = provider_manager
        self.policy = policy

    async def execute(self, capability: str, operation: str, arguments: Dict[str, Any], context: ToolExecutionContext) -> ToolExecutionResult:
        start_time = time.time()
        
        # 1. Resolve capability to specific tool metadata
        metadata = await self.resolver.resolve(capability, operation)
        if not metadata:
            return ToolExecutionResult(
                success=False, result=None, execution_time=time.time() - start_time,
                provider="UNKNOWN", tool_name="UNKNOWN", errors=[f"Capability {capability}.{operation} unresolvable"]
            )

        # 2. Evaluate Policy & Budget
        is_authorized = await self.policy.evaluate(metadata, context)
        if not is_authorized:
            return ToolExecutionResult(
                success=False, result=None, execution_time=time.time() - start_time,
                provider=metadata.provider, tool_name=metadata.name, errors=["Permission denied or budget exceeded"]
            )

        # 3. Fetch Provider
        provider = await self.provider_manager.get_provider(metadata.provider)
        if not provider:
            return ToolExecutionResult(
                success=False, result=None, execution_time=time.time() - start_time,
                provider=metadata.provider, tool_name=metadata.name, errors=["Provider offline or missing"]
            )

        # 4. Execute
        result = await provider.execute(metadata.tool_id, arguments, context)
        
        # 5. Decrement Budget (Mocked via policy inside execution context)
        if context.budget:
            context.budget.max_tool_calls -= 1
            context.budget.max_cost -= result.cost
            
        return result

    async def retry(self, execution_id: UUID) -> ToolExecutionResult:
        pass

    async def timeout(self, execution_id: UUID) -> None:
        pass

    async def cancel(self, execution_id: UUID) -> None:
        pass
