# ADR 026: Knowledge Graph Extensibility

## Context
As agents begin to collaborate, pure vector memory limits complex associative reasoning. We need to lay the groundwork for traversing related entities.

## Decision
We introduce the `MemoryNode` abstraction directly alongside `MemoryEdge`, effectively creating a unified graph abstraction over `BaseMemory` records.
Simultaneously, we introduce stub schemas for `KnowledgeRecord`, `KnowledgeRepository`, and `KnowledgeExtractionJob`. These stubs will remain unimplemented in Sprint 9, serving exclusively as API markers for future Knowledge Graph expansions.

## Consequences
- **Pros:** Prepares the system for native Neo4j or complex SQL graph traversals.
- **Cons:** Introduces abstraction overhead in the immediate term for models that won't be actively populated.
