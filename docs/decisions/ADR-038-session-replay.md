# ADR 038: Session Snapshots and Replay Engine

## Context
Debugging non-deterministic LLM agents is notoriously difficult. If an agent wipes a candidate profile, engineers need to understand exactly what the agent "thought" and "saw" at that exact iteration.

## Decision
We enforce `SessionSnapshots` after every iteration of the `CognitivePipeline`. The `ReplayEngine` consumes these snapshots and historic `ReasoningTraces` to simulate "time-travel". By executing an agent in `ExecutionMode.REPLAY`, the runtime bypasses actual tool execution and injects the historic results back into the pipeline, allowing developers to replay thoughts and reflections frame-by-frame.

## Consequences
- **Pros:** Unmatched debugging capabilities. Enables "resume-from-checkpoint" semantics for paused/failed agents.
- **Cons:** Storage heavy. Requires rigorous JSON serialization of all contexts.
