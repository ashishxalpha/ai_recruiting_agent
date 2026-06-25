# Memory Architecture & Engineering

## High-Level Lifecycle
The lifecycle of all memories traversing the system follows a strict progression:
**Capture** → **Index** → **Retrieve** → **Consolidate** → **Archive** → **Expire**

```mermaid
graph TD
    Application --> MemoryEngine
    MemoryEngine --> PostgresWorkingMemoryStore
    MemoryEngine --> SQLAlchemyMemoryRepository
    MemoryEngine -- "RetrievalPolicy" --> Retrieve
    MemoryEngine --> EventBus
    EventBus -- "MemoryCreated" --> BackgroundEmbeddingJob
    BackgroundEmbeddingJob -- "MemoryIndexed" --> EventBus
    MaintenanceScheduler --> MemoryMaintenanceJob
    ConsolidationScheduler --> MemoryConsolidationJob
```

## Entity Relationship Diagram
```mermaid
erDiagram
    BaseMemory {
        uuid id
        string namespace
        float importance
        float confidence
        int access_count
        float decay_score
        string retention_policy
        string external_reference
    }
    SemanticMemory {
        string content
        string summary
        vector embedding
    }
    MemorySource {
        uuid source_id
        string source_type
        string created_by
        uuid workflow_id
        string model_name
        string prompt_version
        string source_entity
        string source_version
    }
    MemoryNode {
        uuid node_id
        string entity_type
    }
    MemoryEdge {
        uuid source_node_id
        uuid target_node_id
        string relationship_type
        float weight
    }
    KnowledgeRecord {
        uuid id
        string structured_schema
    }

    BaseMemory ||--o{ SemanticMemory : inherits
    BaseMemory ||--|| MemorySource : originates_from
    BaseMemory ||--o{ MemoryNode : represents
    MemoryNode ||--o{ MemoryEdge : links_to
```

## Retrieval Policies & Context
Retrieval operations are explicitly governed by a `RetrievalPolicy` (e.g. `HybridRetrievalPolicy`, `SemanticRetrievalPolicy`, `RecencyRetrievalPolicy`).

Instead of returning raw models, `retrieve()` returns a `MemoryContext` object containing:
- `retrieved_memories`
- `retrieval_strategy`
- `retrieval_reason`
- `confidence`
- `search_statistics`
- `warnings`
- `missing_context`

## Maintenance & Consolidation
The platform supports two massive background operations:
1. **MemoryConsolidationJob**: (1) Insight Extraction, (2) Deduplication, (3) Summarization, (4) Memory Creation.
2. **MemoryMaintenanceJob**: Handles duplicate detection, decay recalculation, stale cleanup, embedding regeneration, and graph integrity validation.
