# Workflow Orchestration Platform

## Overview
The system uses an abstracted `WorkflowEngine` protocol. This ensures business logic remains strictly in the application layer, while the orchestration (routing, pausing, checkpointing) is delegated to infrastructure tools.

## Components
- **Workflow State (`RecruitingWorkflowState`)**: A typed, serializable dictionary passed between nodes.
- **Nodes**: Wrappers around Application Services (e.g. `UploadValidationNode`, `HumanApprovalNode`).
- **Conditional Routing**: Rules determining the next execution path based on the state.
- **Checkpointing**: Persists the workflow state to disk to allow for pauses (Human-in-the-Loop) and recovery.

## LangGraph Integration
LangGraph is the underlying engine implementing `WorkflowEngine`. It uses `StateGraph` to compile nodes and edges into a runnable DAG. All LangChain abstractions are intentionally excluded from the application layer to avoid framework lock-in.

## Human in the Loop
Workflows can pause using the `interrupt()` mechanism in LangGraph. When a node detects conditions requiring human intervention (e.g. confidence < threshold), it pauses the workflow, emits a `WorkflowPaused` event with an `InterruptReason`, and saves a checkpoint. The workflow is later resumed via the `/resume` API endpoint.
