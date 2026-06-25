# ADR 021: LangGraph Integration Constraints

## Context
LangChain and LangGraph provide extensive abstractions (Runnables, Agents, Tools, Memory). Unchecked usage of these abstractions often leads to "framework lock-in" where the business domain becomes deeply coupled to LangChain's rapidly changing internal APIs.

## Decision
We will use LangGraph strictly as a DAG state-machine orchestrator.
1. No LangChain `Agents` or `Tools` in this sprint.
2. Business logic is executed by standard Python functions (Services).
3. The `LangGraphWorkflowEngine` wraps these services into LangGraph Nodes.
4. LangSmith is used purely for tracing the execution of these nodes via standard `@traceable` decorators.

## Consequences
- **Pros:** We get the state-machine benefits of LangGraph (checkpointing, visualization) without the framework lock-in.
- **Cons:** We manually wrap services into nodes instead of using auto-generated LangChain tools.
