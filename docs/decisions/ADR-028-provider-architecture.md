# ADR 028: Tool Provider Architecture & Management

## Context
Tools originate from diverse sources: local python functions, REST APIs, GraphQL, and Model Context Protocol (MCP) servers.

## Decision
We abstract the source of a tool behind a `ToolProvider` interface. A centralized `ProviderManager` is responsible for handling the lifecycle, connection pooling, and background health monitoring of these providers. We explicitly implement `LocalToolProvider` and `MCPToolProvider`.

## Consequences
- **Pros:** Providers can be hot-swapped or reconnected transparently if an external server drops connection.
- **Cons:** Requires active background monitoring (`ToolHealthMonitorJob`) to keep the `ProviderManager` state accurate.
