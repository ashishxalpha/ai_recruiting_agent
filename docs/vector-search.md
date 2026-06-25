# Semantic Search & Match Architecture

This document aggregates the design for the Sprint 5 Embedding & Semantic Search capability.

## Embedding Strategy
We utilize OpenAI's `text-embedding-3-small` to encode text. We store these vectors in PostgreSQL using the `pgvector` extension.
Every vector carries metadata:
- `embedding_version`
- `source_hash`
- `generated_at`

This allows us to track staleness and recalculate embeddings when prompts or models are updated.

## Vector Search & Store Design
PostgreSQL `pgvector` supports indexing. We use the **HNSW** index over `IVFFLAT` because HNSW offers vastly superior query performance and recall at the cost of slower build times and higher memory usage.

## Ranking Engine
The `CandidateRankingEngine` powers the matching algorithm. We retrieve the candidate `FULL_PROFILE` vector utilizing pgvector's cosine distance (`<=>`), then we retrieve sub-vectors in application memory to perform dot-product calculations, formulating a final weighted score (40/25/20/10/5).

## Evaluation Framework
Ranking quality is measured offline or manually via:
- `precision_at_k`: Fraction of relevant candidates in the top K.
- `recall_at_k`: Fraction of total relevant candidates successfully retrieved in top K.
- `ndcg_at_k`: Order-aware ranking metric ensuring the best candidates are ranked at the top.
