# ADR 010: Embedding Strategy

## Context
We need to semantically match candidates against job requirements. Standard keyword matching misses synonyms and conceptual overlaps. We need a strategy to represent text as high-dimensional vectors (embeddings) to facilitate semantic search.

## Decision
We will use OpenAI's `text-embedding-3-small` model with 1536 dimensions as the default embedding provider. 
We will store both **FULL_PROFILE** embeddings and granular section embeddings (e.g., SKILLS, EXPERIENCE, EDUCATION) to support hybrid ranking strategies.

## Consequences
- **Pros**: OpenAI's v3 embeddings provide excellent semantic capture at lower costs and smaller dimensions compared to v2. Granular embeddings allow us to weight experience matching differently from skills matching.
- **Cons**: Vendor lock-in with OpenAI. If we switch providers, all vectors must be regenerated.
