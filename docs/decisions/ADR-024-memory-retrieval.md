# ADR 024: Retrieval Policies and Context

## Context
A fixed hybrid scoring algorithm is too rigid. Different use cases demand different retrieval biases (e.g. strict semantic matching vs chronological recency). Furthermore, raw records lack transparency on *why* they were retrieved.

## Decision
We introduce the `RetrievalPolicy` abstraction. The `MemoryEngine.retrieve()` method explicitly requires a policy (e.g., `SemanticRetrievalPolicy`, `HybridRetrievalPolicy`, `RecencyRetrievalPolicy`).

Instead of returning a list of memories, the engine returns a `MemoryContext` object encapsulating:
- `retrieved_memories`
- `retrieval_strategy`
- `retrieval_reason`
- `confidence`
- `search_statistics`
- `warnings`
- `missing_context`

## Consequences
- **Pros:** Promotes deep explainability and flexibility for downstream MCP agents.
- **Cons:** Increases payload sizes and complexity in orchestration logic.
