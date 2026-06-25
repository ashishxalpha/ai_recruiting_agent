from typing import Protocol, Any, Dict
from src.domain.organization_models import OrganizationPolicy

class AIKernel(Protocol):
    """
    Execution-scoped facade bridging all underlying platforms.
    """
    memory: Any
    workflow: Any
    tools: Any
    coordination: Any
    evaluation: Any
    context_builder: Any
    policy_engine: Any

    async def execute_task(self, task: Dict[str, Any]) -> Any: ...
    async def validate_policy(self, policy: OrganizationPolicy) -> bool: ...
