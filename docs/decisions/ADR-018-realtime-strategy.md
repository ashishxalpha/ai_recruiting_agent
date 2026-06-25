# ADR 018: Realtime Strategy via SSE

## Context
The platform executes complex, long-running workflows (e.g., document parsing, AI extraction, semantic embeddings). The frontend needs to reflect these updates in real-time on the Activity page and Candidate timeline without polling the database every second.

## Decision
We will implement **Server-Sent Events (SSE)** instead of WebSockets.
1. **Unidirectional Need**: The server needs to push workflow updates to the client. The client does not need to push high-frequency realtime data back to the server.
2. **Backend Event Translator**: The backend will include an `EventTranslator` layer. It will listen to raw `DomainEvents` on the `EventBus` and translate them into frontend-safe payloads.
3. **Frontend Hook**: We will build `useSSE(url: string)` to subscribe to the `/api/v1/stream` endpoint, parsing events and updating TanStack Query cache automatically.

## Consequences
- **Pros**: SSE is native to HTTP, easier to load-balance, and avoids the overhead of managing bidirectional WebSocket frames.
- **Cons**: Requires keeping HTTP connections open, which can tie up workers if not handled asynchronously. Fastapi `StreamingResponse` handles this well.
