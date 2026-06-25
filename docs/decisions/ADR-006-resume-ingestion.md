# ADR 006: Resume Ingestion and Candidate Decoupling

**Date:** 2026-06-24
**Status:** Accepted

## Context
Initially, the system created a `Candidate` entity immediately upon resume upload. However, because the system relies on AI extraction to populate Candidate details (like Name, Email, Phone), creating an empty Candidate at upload leads to partial records that break validation and business rules.

## Decision
We decouple the Candidate entity from the initial upload process.
1. The upload creates a `CandidateDocument` with an optional `candidate_id`.
2. A new entity `ResumeIngestionRequest` tracks the asynchronous parsing pipeline.
3. Once the `BackgroundJob` completes the AI Extraction, a populated `Candidate` is created and linked to the `CandidateDocument`.

## Consequences
- **Pros:** Candidate entities are always fully populated and valid. Ingestion lifecycle is explicitly tracked.
- **Cons:** API clients must track `ingestion_id` or `job_id` rather than a `candidate_id` immediately.
