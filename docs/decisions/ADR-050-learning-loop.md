# ADR 050: Learning Loop Without Online Training

## Context
If we train the models online as they run, we introduce catastrophic forgetting, indeterminism, and massive cost spikes. However, the organization must still "learn" from its executions.

## Decision
We implement a `LearningLoop` driven entirely by `MemoryEngine` consolidation and Metrics generation. After every `OrganizationExecution`, a Reflection sequence evaluates the outcome. Insights are persisted as long-term Semantic Memory. Skill and Role metrics (latency, success rates, token cost) are updated.

## Consequences
- **Pros:** 100% deterministic model states. "Learning" is isolated to retrieval context (RAG) rather than weight updates.
- **Cons:** Prompts may grow longer over time as the organization retrieves more historic context to avoid past mistakes.
