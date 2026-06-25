# ADR-009: Dead Letter Queue (DLQ) for Failed Extractions

## Context
During background processing of resume extractions, jobs may fail due to unpredictable issues: corrupted PDF files, extreme token length causing context-window limits, or OpenAI API being completely unreachable despite retries. If these jobs simply enter a `FAILED` state without capturing the context of the failure, it becomes extremely difficult for engineers to debug or for system administrators to manually trigger retries.

## Decision
We will introduce a **FailedExtractionTrackingProvider** abstraction to act as a Dead Letter Queue (DLQ). When a background job fails all retries in the `ResumeExtractionWorkflow`, the exception details, payload, and document context are shipped to this DLQ provider.

## Consequences
- **Pros**: Ensures no failed resume is silently lost. Enables the future development of an admin dashboard to review failed parsing attempts and re-trigger them after fixes.
- **Cons**: Adds an extra required dependency to the workflow layer. Requires implementing a concrete backend (e.g., a specific database table or AWS SQS queue) in a later sprint.
