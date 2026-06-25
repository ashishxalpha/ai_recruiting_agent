# ADR 034: Execution Budget

## Context
Unbounded tool execution can result in infinite agent loops, racking up catastrophic token or infrastructure costs.

## Decision
We introduce the `ExecutionBudget` context object, tracking `max_cost`, `max_tokens`, `max_tool_calls`, and `timeout`.
The `ToolPolicy` interceptor natively tracks and decrements this budget during every execution. If the budget is exhausted, execution is hard-blocked.

## Consequences
- **Pros:** Hard safety guarantees preventing runaway LLM processes.
- **Cons:** Requires highly accurate cost/token estimations from the underlying `ToolProvider`.
