# ADR 012: Hybrid Ranking Algorithm

## Context
When a recruiter searches for candidates matching a job requirement, ordering solely by vector similarity can sometimes push candidates with perfect specific skills lower if their summary doesn't align nicely in semantic space. We need a ranking mechanism that accounts for multiple dimensions.

## Decision
We implemented a hybrid ranking engine that uses the following weighted score:
- **Vector Similarity (40%)**: Cosine similarity of the `FULL_PROFILE` embeddings.
- **Skills Match (25%)**: Similarity between the extracted skills vector and the requirement.
- **Experience Match (20%)**: Similarity between the extracted experience vector and the requirement.
- **Education Match (10%)**: Similarity between the extracted education vector and the requirement.
- **Profile Quality (5%)**: Extracted `overall_confidence` score from the validation layer.

## Consequences
- **Pros**: More accurate and customizable matching algorithm that mirrors human recruiter logic.
- **Cons**: Requires fetching and generating multiple embedding vectors per candidate and job, increasing compute and storage costs.
