# ADR 044: Shared Context Versioning & Scoping

## Context
When multiple agents collaborate on a task, they need a scratchpad to share temporary variables (e.g., extracted tokens, intermediate reasoning). If this is written directly to the MemoryEngine, the long-term semantic memory becomes polluted with transient garbage. If they mutate a single shared dictionary, race conditions occur.

## Decision
We introduce `SharedContext` snapshots with a predefined scope (`GLOBAL`, `SESSION`, `TASK`, `AGENT`). Every time an agent updates the shared context, a new immutable snapshot is generated. The `SharedContextCleanupJob` natively sweeps old data using a configurable TTL (default 48 hours) to prevent state buildup.

## Consequences
- **Pros:** Perfect auditability. Eliminates race conditions. Keeps `MemoryEngine` pristine.
- **Cons:** Rapidly expanding database footprint during high-concurrency executions.
