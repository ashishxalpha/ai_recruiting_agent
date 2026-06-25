# ADR 040: Multi-Agent Coordination Platform

## Context
Running multiple intelligent agents requires strict supervisory infrastructure. Without it, agents may enter infinite argument loops, duplicate effort, or lock system resources.

## Decision
We introduce the `Multi-Agent Coordination Platform`. It explicitly enforces a master-worker dynamic where a `Supervisor` orchestrates work by decomposing `Goals` into a `DelegationPlan` and assigning tasks. Agents never directly command other agents; all coordination flows up to the Supervisor and through the `AgentCommunicationBus`.

## Consequences
- **Pros:** Hard safety limits on swarm behavior. Infinite loops are intercepted by the `ConflictResolver` and `Supervisor`.
- **Cons:** Centralized bottleneck during high-volume message passing.
