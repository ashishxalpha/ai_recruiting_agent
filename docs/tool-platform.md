# Enterprise Tool Platform Architecture

## High-Level Execution Flow
Workflows request operations via capabilities. The system dynamically resolves, secures, and executes the capability via independent providers. The `ContextBuilder` pre-assembles all execution parameters before invoking the `ToolExecutor`.

```mermaid
graph TD
    Workflow --> ContextBuilder
    ContextBuilder -- "Assembles Unified Context" --> CapabilityResolver
    CapabilityResolver -- resolves --> ToolRegistry
    Workflow --> ToolExecutor
    ToolExecutor --> ToolPolicy
    ToolPolicy --> PermissionStore
    ToolPolicy -- "Validates Budget & Policy" --> ProviderManager
    ProviderManager --> MCPToolProvider
    ProviderManager --> LocalToolProvider
```

## Entity Relationship Diagram
```mermaid
erDiagram
    ToolSession {
        uuid id
        uuid workflow_id
        uuid execution_id
        float duration
        float total_cost
        json tools_used
    }
    ExecutionBudget {
        float max_cost
        int max_tokens
        int max_tool_calls
        int timeout
    }
    ToolMetadata {
        string tool_id
        string execution_target
        boolean approval_required
    }
    ToolContract {
        json input_schema
        json output_schema
        json examples
        string version
        json error_codes
    }
    ToolExecutionResult {
        boolean success
        json result
        json artifacts
        json logs
        json metrics
        json references
    }
    ToolPipeline {
        uuid pipeline_id
        json execution_chain
    }

    ToolMetadata ||--|| ToolContract : defines
    ToolSession ||--o{ ToolExecutionResult : tracks
    ToolSession ||--|| ExecutionBudget : constrained_by
```

## Sequence Diagram: Tool Execution
```mermaid
sequenceDiagram
    participant Agent as Workflow
    participant CB as ContextBuilder
    participant CR as CapabilityResolver
    participant TE as ToolExecutor
    participant TP as ToolPolicy
    participant PM as ProviderManager
    participant P as Provider

    Agent->>CB: assemble_context()
    CB-->>Agent: UnifiedExecutionContext
    Agent->>CR: resolve("filesystem", "read")
    CR-->>Agent: {"provider": "mcp_file", "tool": "read_file"}
    Agent->>TE: execute("read_file", context)
    TE->>TP: evaluate_policy(context, budget)
    TP-->>TE: Authorized
    TE->>PM: get_provider("mcp_file")
    PM-->>TE: Provider Instance
    TE->>P: execute("read_file", args)
    P-->>TE: Output
    TE->>Agent: ToolExecutionResult
```
