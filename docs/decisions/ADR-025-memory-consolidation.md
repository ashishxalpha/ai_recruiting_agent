# ADR 025: Memory Consolidation and Maintenance

## Context
Active memory environments suffer from redundancy, drift, and latency degradation over time without maintenance.

## Decision
We enforce two distinct background lifecycle jobs:
1. **MemoryConsolidationJob**: Migrates high-activity episodic states into dense semantic blobs. Process: `Insight Extraction` -> `Deduplication` -> `Summarization` -> `Memory Creation`.
2. **MemoryMaintenanceJob**: A system hygiene process managing `duplicate detection`, `decay recalculation`, `stale memory cleanup`, `embedding regeneration` (when models upgrade), and `graph integrity validation`.

## Consequences
- **Pros:** System memory remains pristine, fast, and highly relevant. Prevents "hallucination poisoning" over time.
- **Cons:** Massive background compute requirements. Maintenance failures could sever graph edges.
