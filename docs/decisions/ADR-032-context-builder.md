# ADR 032: Context Builder Orchestration

## Context
Executing a tool securely requires resolving a massive payload of contextual data (Agent Memory, Workflow State, API Credentials, User Context). Passing these individually into the `ToolExecutor` is fragile and leads to brittle function signatures.

## Decision
We introduce the `ContextBuilder` abstraction. Before execution, the orchestrator invokes the `ContextBuilder` which asynchronously gathers `MemoryContext`, `WorkflowContext`, `UserContext`, and `SystemContext`, packing them into a unified, frozen `ToolExecutionContext`.

## Consequences
- **Pros:** The `ToolExecutor` receives a single immutable context object. Easy to test and mock.
- **Cons:** Adds an additional network hop/latency step before every tool invocation.
