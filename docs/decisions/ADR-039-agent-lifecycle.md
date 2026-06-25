# ADR 039: Agent Lifecycle States

## Context
Background processes require robust state management to survive system restarts, pauses for human approval, or unexpected crashes.

## Decision
Agents adhere to a strict State Machine defined by `AgentLifecycle`. Transitions are validated by the `AgentRuntime`:
`CREATED` -> `INITIALIZING` -> `READY` -> `RUNNING` -> `WAITING` | `PAUSED` -> `FAILED` | `STOPPED` | `TERMINATED`.

## Consequences
- **Pros:** We can safely pause agents (`PAUSED`), await asynchronous events (`WAITING`), and gracefully shutdown clusters without leaving zombie states.
- **Cons:** Adds complexity to the API layer, which must now check agent states before issuing commands.
