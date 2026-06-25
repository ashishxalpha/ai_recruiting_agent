# ADR 045: Supervisor Abstraction

## Context
A cluster of agents cannot self-organize without a designated leader tracking the ultimate goal.

## Decision
We introduce the `Supervisor`. The Supervisor is NOT an agent—it performs no reasoning. It acts strictly as an orchestrator. It receives `Goals`, triggers the `GoalEngine`, delegates tasks using the `DelegationEngine`, and aggregates results. It then triggers the `ConsensusEngine` to finalize the goal state. 

## Consequences
- **Pros:** Strict separation of coordination mechanics from LLM reasoning limits token spend and isolates orchestration logic.
- **Cons:** Centralized point of failure for a coordination session.
