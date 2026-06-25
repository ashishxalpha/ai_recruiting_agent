# ADR 005: Database Design for AI Copilot

**Date:** 2026-06-24
**Status:** Accepted

## Context
We need a scalable and robust database schema to support complex entity relationships (Candidates, Skills, Documents, Extractions). Using integer IDs across distributed microservices can lead to collision and enumeration attacks. Deleting records forcefully can cause loss of historical data and audit trails.

## Decision
We will use:
1. **UUIDs** as primary keys for all tables.
2. **Soft Deletes**: Every major entity features a `deleted_at` timestamp. Records are never `DELETE`d via SQL.
3. **Audit Trails**: All modifications (CREATE, UPDATE, DELETE) are logged via an `AuditLog` table containing a `JSONB` payload of changes.

## Consequences
- **Pros:** Better security, easy data recovery, comprehensive auditability, scalable primary key generation.
- **Cons:** Queries must always explicitly filter `deleted_at IS NULL` (often handled transparently in repositories).
