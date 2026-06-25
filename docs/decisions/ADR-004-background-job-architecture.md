# ADR 004: Background Job Architecture

**Date:** 2026-06-24
**Status:** Accepted

## Context
Resume ingestion and AI extraction are heavy operations. They should be offloaded to background workers to prevent blocking API requests. In the early stages, deploying a full message broker (like RabbitMQ or Redis) and a worker fleet (like Celery) is overkill and increases infrastructure complexity.

## Decision
We will define domain-level abstractions for background jobs (`BackgroundJob` entity, `JobRepository`, and a job execution interface). For the initial phase, we will utilize FastAPI's built-in `BackgroundTasks` to execute jobs asynchronously within the same process. When the load increases, the abstraction will seamlessly allow swapping the execution mechanism to Celery, Dramatiq, or ARQ.

## Consequences
- **Pros:** Keeps initial infrastructure simple while preserving the ability to scale later.
- **Cons:** Jobs are lost if the backend process crashes during execution. This is acceptable for Phase 1.
