# ADR 019: Workflow Engine Orchestration Abstraction

## Context
The system currently uses hardcoded, static workflows (e.g. `ResumeExtractionWorkflow`). As we move towards more complex pipelines, multi-agent systems, and dynamic routing, hardcoded procedural workflows are brittle and difficult to observe.

## Decision
We will introduce a `WorkflowEngine` Protocol. The application layer will depend ONLY on `WorkflowEngine`. LangGraph will be used as the underlying orchestration engine (`LangGraphWorkflowEngine`), but it will be strictly isolated to the Infrastructure layer.

## Consequences
- **Pros:** Business logic remains in pure Python application services. The orchestrator can be swapped or tested in isolation. Prevents leaking LangChain/LangGraph abstractions into domain code.
- **Cons:** Adds an abstraction layer and requires wrapping LangGraph nodes explicitly.
