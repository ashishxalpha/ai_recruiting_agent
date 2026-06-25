# ADR 043: Consensus Engine

## Context
When multiple agents collaborate on a single goal (e.g., scoring a candidate profile), they may return wildly different results.

## Decision
We introduce the `ConsensusEngine`. Supervisors collect task results and pass them to the engine, which executes a pluggable strategy (`MajorityVote`, `HighestConfidence`, `WeightedScore`, or `HumanApproval`). If consensus fails, the issue is escalated to the `ConflictResolver`.

## Consequences
- **Pros:** Guarantees deterministic, resolved outputs before returning a goal as COMPLETED.
- **Cons:** Requires rigorous defining of vote schemas.
