# ADR 030: Tool Security and Permission Policies

## Context
Executing code or interacting with external systems via tools carries massive security risks (e.g., an agent wiping a filesystem or leaking a database). Simple boolean checks are insufficient.

## Decision
We mandate a `ToolPolicy` interceptor inside the `ToolExecutor`. The policy queries a swappable `PermissionStore` (which can be static, RBAC, or ABAC). 
The `ToolPolicy` asserts:
1. Does the execution context possess the required permission scope?
2. Does the tool configuration require explicit human approval (`ApprovalRequired`)?
3. Does the execution exceed configured rate limits, timeouts, or cost ceilings?

## Consequences
- **Pros:** Zero-trust architecture. Tool execution is provably secure regardless of what the LLM or Workflow attempts to do.
- **Cons:** The policy evaluation must be highly performant to prevent latency degradation on rapid tool use.
