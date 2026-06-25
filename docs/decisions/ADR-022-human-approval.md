# ADR 022: Human-in-the-Loop Orchestration

## Context
When AI extraction or matching confidence falls below a configured threshold, the workflow must halt and wait for a recruiter's explicit approval or adjustment.

## Decision
We will implement Human-in-the-Loop using LangGraph's inherent interrupt mechanisms. 
1. The `ProfileEvaluationNode` checks the confidence score against a dynamic configuration threshold.
2. If it falls below, a conditional edge routes to `HumanApprovalNode`.
3. `HumanApprovalNode` triggers an interrupt, setting `workflow_status` to `PAUSED` and an `interrupt_reason` (e.g. `LOW_CONFIDENCE`).
4. The API exposes `POST /api/v1/workflows/{id}/resume` which supplies the human feedback and continues the graph execution.

## Consequences
- **Pros:** Avoids manual polling. Leverages the robust CheckpointSaver to suspend execution safely across server restarts.
- **Cons:** Requires strict adherence to the `RecruitingWorkflowState` to ensure the human feedback correctly mutates the frozen state upon resumption.
