# ADR 013: Feedback Architecture

## Context
We need to capture recruiter feedback on AI-generated candidate matches to learn recruiter preferences and evaluate the ranking algorithm. Originally, matches were transient. To attach feedback, matches must be persisted and immutable.

## Decision
1. **SearchSessions**: Introduce a `SearchSession` entity. Every search request generates a new session.
2. **Immutable Candidate Matches**: `CandidateMatch` and `MatchExplanation` will be tied to a `SearchSession`. They are immutable and never overwritten. If the ranking algorithm changes, a new search will generate a new session and new match versions.
3. **Domain Events**: When feedback is submitted, a `RecruiterFeedbackSubmitted` domain event is published. This allows decoupled services (e.g., future memory systems, `RecruiterPreferenceService`) to learn from the feedback without tight coupling.

## Consequences
- **Pros**: Full historical audit trail of what the AI presented and how the recruiter responded. Supports time-travel debugging and future learning layers.
- **Cons**: High database growth since every search query persists multiple matches and explanations. Will require data retention policies or archival strategies in the future.
