from src.application.tools.interfaces import ToolPolicy, ToolExecutionContext, PermissionStore
from src.domain.tool_models import ToolMetadata

class DefaultToolPolicy(ToolPolicy):
    def __init__(self, permission_store: PermissionStore):
        self.permission_store = permission_store

    async def evaluate(self, tool: ToolMetadata, context: ToolExecutionContext) -> bool:
        # 1. Budget validation
        if context.budget:
            if context.budget.max_tool_calls <= 0:
                return False
            if context.budget.max_cost <= 0:
                return False
                
        # 2. Permission validation
        allowed_capabilities = await self.permission_store.get_allowed_capabilities(context)
        
        # Check if the tool capabilities intersect with the allowed capabilities
        has_permission = any(cap in allowed_capabilities for cap in tool.capabilities)
        if not has_permission and "*" not in allowed_capabilities:
            return False
            
        # 3. Approval Requirements
        if tool.approval_required:
            # We would pause here or reject if context doesn't contain an approval override
            pass
            
        return True
