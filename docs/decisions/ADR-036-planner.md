# ADR 036: Pluggable Planner & Cognitive Pipeline

## Context
Agents require a reasoning loop to decide what to do next. Hardcoding a specific LLM chain or LangGraph flow permanently binds the agent to one mode of reasoning (e.g., ReAct). As models evolve, we may want Tree-of-Thoughts, Graph reasoning, or deterministic Rule-based planning.

## Decision
We abstract reasoning into a `CognitivePipeline` containing explicit, pluggable stages: Observe -> Retrieve -> Reason -> Plan -> Execute -> Reflect -> Learn. The `Plan` phase is delegated to a `Planner` interface. Initially, we implement `RulePlanner` utilizing simple JSON decision trees (from `AgentTemplate`) to allow deterministic execution before hooking up expensive LLMs.

## Consequences
- **Pros:** We can benchmark different Planners against the exact same agent tasks. Supports deterministic testing via RulePlanner.
- **Cons:** Increases boilerplate required to define an agent's reasoning capacity.
