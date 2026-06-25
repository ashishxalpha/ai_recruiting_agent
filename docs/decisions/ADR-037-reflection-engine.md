# ADR 037: Reflection Engine

## Context
Executing actions without analyzing the result prevents agents from self-correcting.

## Decision
We mandate a `ReflectionEngine` at the end of the `CognitivePipeline`. The engine consumes the `ReasoningTrace` (containing the Observation, Plan, Action, and Result), generates an `AgentReflection`, and updates the agent's internal `WorkingMemory`. Initially implemented as `RuleReflectionEngine`, it lays the groundwork for LLM-based self-critique.

## Consequences
- **Pros:** Native self-correction loop. Generates incredibly valuable ground-truth data for future model fine-tuning.
- **Cons:** Doubles the LLM token overhead during reasoning loops once LLM reflection is enabled.
