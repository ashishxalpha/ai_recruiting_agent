# ADR 020: Checkpoint Strategy

## Context
Long-running workflows (especially those waiting on human approval) must be able to pause, suspend to disk, and resume. They also need to recover from infrastructure failures.

## Decision
We introduce a `CheckpointStore` protocol in the application layer. The implementation, `DatabaseCheckpointStore`, will live in the infrastructure layer and explicitly implement LangGraph's `BaseCheckpointSaver`. This allows LangGraph to natively handle state persistence while keeping the application ignorant of LangGraph's internal `CheckpointTuple` representations.

## Consequences
- **Pros:** True resume/replay capabilities. Robust error recovery.
- **Cons:** The state must be 100% serializable (no raw DB sessions or open file handles in the `RecruitingWorkflowState`).
