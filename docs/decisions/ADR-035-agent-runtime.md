# ADR 035: Agent Runtime Platform

## Context
Future agents will execute deeply complex, long-running processes requiring explicit monitoring, throttling, and concurrency control. Tying agent execution directly into web endpoints or scattered background jobs leads to untraceable zombie processes.

## Decision
We introduce the `AgentRuntime` as the core execution supervisor, backed by a `RuntimeScheduler`. The Runtime manages the `AgentLifecycle` (CREATED -> RUNNING -> PAUSED -> TERMINATED). The scheduler handles queueing, concurrency, and throttling across multiple simultaneous agent sessions.

## Consequences
- **Pros:** Full control over agent computing resources. Enables explicit Start/Pause/Resume semantics via APIs.
- **Cons:** High infrastructure footprint. Introduces complex state machine handling.
