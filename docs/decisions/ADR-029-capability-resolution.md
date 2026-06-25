# ADR 029: Capability Resolution

## Context
If an agent hardcodes a tool request (e.g. `execute("google_calendar_create_event")`), it breaks when the organization migrates to Microsoft Outlook.

## Decision
We enforce a capability hierarchy: `Capability -> Provider -> Tool -> Operation`. Agents request an abstract capability (e.g. `capability="scheduling", operation="create_event"`). The `CapabilityResolver` maps this dynamically to the active provider (e.g. `mcp_outlook_server`) via the `ToolRegistry`.

## Consequences
- **Pros:** Total abstraction. We can swap underlying providers (e.g. migrating from Local file reading to an MCP File server) without rewriting a single agent prompt or workflow logic.
- **Cons:** Requires rigorous standardization of `input_schema` across tools mapped to the same capability.
