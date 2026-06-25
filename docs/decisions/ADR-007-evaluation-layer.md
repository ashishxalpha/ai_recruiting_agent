# ADR-007: Evaluation Layer for AI Extraction

## Context
When processing resumes with an AI Provider, the output may have varying levels of completeness and quality. Some resumes might be incomplete, and AI hallucinations are possible. We need a way to track the confidence of the parsed results and potentially flag Candidate profiles for manual review rather than failing the pipeline completely or silently accepting bad data.

## Decision
We will introduce an **Evaluation Layer** after validation. 

1. **ProfileEvaluator**: A service that assesses the `CandidateProfile` against a set of heuristics (and potentially secondary LLM calls in the future).
2. **ProfileEvaluationResult**: A data structure capturing `confidence_score`, `completeness_score`, `quality_score`, `warnings`, and `issues`.
3. **Storage**: The evaluation scores will be persisted inside the `AIExtraction` database record for analytical tracking.

## Consequences
- **Pros**: It allows the system to gracefully handle bad resumes. It surfaces confidence scores that can be displayed to reviewers.
- **Cons**: Adds another layer of complexity to the background processing pipeline. Heuristic-based evaluations may require tuning over time.
