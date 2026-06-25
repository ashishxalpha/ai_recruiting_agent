# ADR 041: Agent Communication Bus & Mailboxes

## Context
If Agent A calls a python function on Agent B directly, the system becomes tightly coupled and impossible to distribute across a cluster.

## Decision
Agents communicate asynchronously over the `AgentCommunicationBus`. Messages are classified by type (`COMMAND`, `REQUEST`, `RESPONSE`, `EVENT`, `BROADCAST`). Every agent instance maintains a durable `AgentMailbox` to enqueue inbound messages and allow the `AgentRuntime` to pull tasks sequentially.

## Consequences
- **Pros:** Agents can be distributed across nodes or clusters trivially. Mailboxes allow asynchronous pausing and resuming.
- **Cons:** Latency overhead. Message schemas must be strictly validated.
