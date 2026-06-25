# ADR 033: Tool Pipeline Abstraction

## Context
Agents often chain tool calls (e.g., Read File -> Summarize -> Search Web -> Write File). Managing this sequentially within a LangGraph node is cumbersome.

## Decision
We introduce the `ToolPipeline` abstraction. This is a stub for future orchestration that allows multiple tool invocations to be chained together atomically within the Tool Platform layer itself.

## Consequences
- **Pros:** Prepares the system for advanced orchestration operations (like map-reduce tool executions).
- **Cons:** Will not be fully implemented in this sprint, serving purely as an architectural marker.
