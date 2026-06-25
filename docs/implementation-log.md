# Implementation Log

## Phase 1: Candidate Resume Ingestion and Structured Resume Parsing

### Sprint 1: Bootstrap & Infrastructure Setup
- **[DONE]** Created initial documentation (Architecture, Folder Structure, API Reference, Implementation Log).
- **[DONE]** Create ADR for Domain-Driven Design and Async Workflow.
- **[DONE]** Initialize Next.js 15+ frontend.
- **[DONE]** Initialize FastAPI backend with `uv`.
- **[DONE]** Setup `docker-compose.yml` for PostgreSQL.

### Sprint 2: Core Domain Models, Database Design & Infrastructure
- **[DONE]** Created domain entities and enums (Candidate, CandidateDocument, BackgroundJob, etc).
- **[DONE]** Implemented SQLAlchemy 2.0 models with Alembic migrations setup.
- **[DONE]** Created Repository Contracts and implemented `CandidateRepository`.
- **[DONE]** Created Storage Abstraction and `LocalStorageProvider`.
- **[DONE]** Built OpenTelemetry observability foundation (logging, tracing, metrics).
- **[DONE]** Fully Dockerized backend (`Dockerfile`) and frontend (`Dockerfile.dev`, `Dockerfile`).
- **[DONE]** Updated documentation (ER diagrams, Domain diagrams, new ADRs).
