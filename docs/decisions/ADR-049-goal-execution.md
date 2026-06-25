# ADR 049: Goal Execution & Pipelines

## Context
We need a mechanism to transition from a high-level intent ("Process this candidate") down to local execution of python functions without leaking orchestration logic into the roles.

## Decision
We construct a `SkillDependencyGraph`. A `GoalTemplate` maps high-level goals to this graph. The `SkillPipeline` resolves execution. By default, pipelines execute locally inside the single role's process space to save latency. Only parallel or cross-role dependencies escalate via the `CoordinationPlatform`.

## Consequences
- **Pros:** Massive reduction in message bus latency for purely sequential operations while retaining the ability to distribute out to the cluster automatically.
- **Cons:** Complex dynamic pipeline routing logic required.
