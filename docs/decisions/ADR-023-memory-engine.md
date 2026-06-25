# ADR 023: Memory Engine Architecture

## Context
Future iterations of this platform will feature multi-agent swarms, MCP servers, and extensive graph workflows. Exposing memory functionality directly via LangGraph abstractions tightly couples memory strictly to workflow nodes, preventing decoupled services (like a backend background job) from manipulating long-term memory contexts.

## Decision
We decouple memory generation, persistence, and retrieval from LangGraph. We introduce a `MemoryEngine` interface, serving as the sole broker of system memory. `MemoryEngine` will support distinct memory subclasses: `SemanticMemory`, `EpisodicMemory`, `ProceduralMemory`, and `WorkingMemory`. Working memory will utilize a dedicated `WorkingMemoryStore` protocol.
When memories are stored, `MemoryEngine` synchronously persists the metadata but defers embedding generation via a `MemoryCreated` event to avoid blocking core execution pipelines.

## Consequences
- **Pros:** Total independence from LangGraph. Memory can be seamlessly manipulated by any component. Vectorization scales horizontally via background workers.
- **Cons:** Introduces eventual consistency into the semantic search indexing process.
