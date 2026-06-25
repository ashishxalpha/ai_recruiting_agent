# Background Job System

To process long-running tasks like AI Extractions, we use an asynchronous job execution system.

## Framework Independence
The system is built on a framework-independent `JobDispatcher` protocol.
Currently, it uses `FastAPIJobDispatcher` which relies on FastAPI's native `BackgroundTasks`.

In future sprints, this can be swapped with:
- Celery
- ARQ
- LangGraph

All implementations must satisfy:
```python
class JobDispatcher(Protocol):
    async def dispatch(self, job_name: str, payload: dict) -> None: ...
```

## Lifecycle statuses
A job transitions through: `PENDING` -> `QUEUED` -> `RUNNING` -> `COMPLETED` (or `FAILED` / `CANCELLED` / `RETRYING`).
