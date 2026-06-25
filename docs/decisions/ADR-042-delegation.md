# ADR 042: Goal-Driven Delegation Engine

## Context
If a Supervisor arbitrarily hardcodes which agent gets which task, the system breaks whenever an agent is busy or offline. 

## Decision
We introduce the `GoalEngine` to maintain task dependency graphs. The `DelegationPlanner` decomposes these goals into sub-tasks. The `DelegationEngine` dynamically discovers appropriate agents using the `AgentContract` (matching capabilities and availability statuses like `online`, `busy`, `degraded`) to assign tasks dynamically.

## Consequences
- **Pros:** Highly resilient swarm. If an agent goes offline, the `DelegationEngine` simply re-routes the task to another agent holding the required capability.
- **Cons:** Complex capability-matching logic is required.
