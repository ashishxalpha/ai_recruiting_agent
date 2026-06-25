# ADR 031: MCP Integration Strategy

## Context
The Model Context Protocol (MCP) defines a powerful standard for exposing tools and resources to LLMs. However, utilizing MCP directly as the core system architecture tightly couples the internal agent logic to external server lifecycles, and makes supporting non-MCP endpoints (like local functions or GraphQL) difficult.

## Decision
MCP is treated strictly as **one type of provider** (`MCPToolProvider`). The `MCPToolProvider` utilizes the official Python SDK, supporting configurable transports (`stdio`, `SSE`, `WebSocket`). The application layer interacts with the `ToolProvider` protocol, completely oblivious to whether the underlying tool is an MCP server or a local python function.

## Consequences
- **Pros:** Full adoption of the MCP standard without architectural lock-in. Immediate support for the global ecosystem of MCP servers (GitHub, Postgres, Filesystem).
- **Cons:** We must map MCP's native JSON-RPC schemas into our internal `ToolMetadata` and `ToolExecutionResult` standards.
