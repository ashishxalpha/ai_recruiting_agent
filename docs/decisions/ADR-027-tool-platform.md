# ADR 027: Enterprise Tool Platform Independence

## Context
Tools allow agents to manipulate the outside world. Tying tool execution directly to an agent orchestration framework (like LangGraph) tightly couples business capabilities to orchestration logic, making tools difficult to test, secure, and monitor outside of an active agent session.

## Decision
We introduce an independent Enterprise Tool Platform. All tool executions must be requested via a `CapabilityResolver` and pass through a centralized `ToolExecutor` and `ToolPolicy` interceptor before reaching a `ToolProvider`.

## Consequences
- **Pros:** Tools can be executed by REST clients, background jobs, or distinct agent frameworks interchangeably. Unified observability and security.
- **Cons:** High level of indirection. Executing a tool requires traversing Resolver -> Executor -> Policy -> Provider Manager -> Provider.
