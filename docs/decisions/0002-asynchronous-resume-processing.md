# ADR 0002: Asynchronous Resume Processing Workflow

**Date:** 2026-06-24
**Status:** Accepted

## Context
Resume ingestion involves parsing documents (PDF/DOCX) and sending the extracted text to an AI model (OpenAI) to generate structured outputs. This process is highly variable in latency and can take anywhere from a few seconds to over a minute per document. Doing this synchronously within the HTTP request cycle would result in poor user experience, timeouts, and blocked API threads.

## Decision
We will adopt an asynchronous workflow for resume ingestion:
1. User uploads a file via `POST /api/v1/resumes/upload`.
2. Backend saves the file to a storage provider, creates a `Candidate` record with status `PROCESSING`, and enqueues a background task.
3. The API immediately returns `202 Accepted` with a `candidate_id`.
4. A background worker (e.g., using Celery, RQ, or FastAPI `BackgroundTasks` for phase 1) picks up the job, extracts text, calls the AI provider, and updates the `ai_extractions` and `candidates` tables.
5. The frontend polls or uses WebSockets (initially polling via `GET /api/v1/candidates/{id}/status`) to check the status and displays the result when `PROCESSED`.

## Consequences
- **Pros:** Scalable, resilient to AI provider latency, better user experience (no blocked UI).
- **Cons:** Requires background task infrastructure, polling mechanism on frontend, and more complex state management (`PROCESSING`, `FAILED`, `PROCESSED`).
