# ADR 011: Vector Store Design

## Context
With embeddings generated, we need a vector database to perform nearest-neighbor searches (ANN). Options include dedicated databases like Pinecone, Milvus, or Qdrant, or extending our existing PostgreSQL database with `pgvector`.

## Decision
We will use `pgvector` inside our existing PostgreSQL instance. We will configure an **HNSW** (Hierarchical Navigable Small World) index for fast approximate nearest neighbor search, with an `IVFFLAT` fallback strategy if HNSW memory requirements become an issue at immense scale.

## Consequences
- **Pros**: Simplifies infrastructure by avoiding a separate database service. Simplifies data consistency—candidate records and vectors are in the same ACID-compliant store.
- **Cons**: `pgvector` increases the load on our primary transactional database. Scaling vector search might eventually require read-replicas or a dedicated instance.
