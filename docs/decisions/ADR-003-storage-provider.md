# ADR 003: Storage Provider Abstraction

**Date:** 2026-06-24
**Status:** Accepted

## Context
Resume ingestion requires persisting physical documents (PDF/DOCX) before extraction. In local development, these files can be stored on disk. However, in production, a cloud storage solution like AWS S3, Cloudflare R2, or MinIO is required. Hardcoding file I/O operations will lead to a highly coupled architecture.

## Decision
We will define a generic `StorageProvider` interface in the domain layer. The implementation is injected during application initialization. For Sprint 2, we implement `LocalStorageProvider` mapping to Docker mounted volumes (`/storage/resumes`, `/storage/documents`).

## Consequences
- **Pros:** Easy to switch to cloud storage providers later without modifying core business logic.
- **Cons:** Requires slight indirection for simple local I/O operations.
