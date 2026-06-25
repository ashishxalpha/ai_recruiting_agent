# ADR 014: Ground Truth Timeline Design

## Context
Originally, we planned a singular `GroundTruthOutcome` for a Candidate/Job pairing. However, recruitment is a timeline. A candidate applies, is interviewed, might be offered, and might accept or decline. Overwriting a singular "outcome" loses the chronological resolution necessary to train AI models on conversion funnels.

## Decision
We will replace `GroundTruthOutcome` with a `GroundTruthEvent` model that functions as an append-only timeline log.
Events include: `APPLIED`, `INTERVIEWED`, `OFFERED`, `ACCEPTED`, `HIRED`, `REJECTED`, `WITHDRAWN`.
Every event triggers a `GroundTruthRecorded` domain event.

## Consequences
- **Pros**: We can measure funnel drop-off and identify *where* the AI failed (e.g. AI recommended highly, recruiter interviewed, but candidate failed technical interview vs candidate withdrew).
- **Cons**: Queries for "final state" become more complex (requiring fetching the latest event in the timeline rather than a static column).
