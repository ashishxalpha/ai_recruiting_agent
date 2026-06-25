# ADR 0001: Use Domain-Driven Design for Backend

**Date:** 2026-06-24
**Status:** Accepted

## Context
The AI Recruiting Copilot Platform requires a robust and maintainable backend architecture. As the platform evolves to include matching, memory, and RAG capabilities, the business logic will become complex. Mixing business logic with framework-specific code (e.g., FastAPI routing) or ORM models (SQLAlchemy) will lead to an unmaintainable monolith.

## Decision
We will adopt a layered Domain-Driven Design (DDD) architecture. The application will be split into:
1. **Domain**: Core entities and interfaces, purely Python, zero external dependencies where possible.
2. **Application**: Use cases, orchestrating business logic without knowing infrastructure details.
3. **Infrastructure**: Implementations of database access (SQLAlchemy repositories), third-party API clients (OpenAI), and parsing (PyMuPDF, python-docx).
4. **Presentation**: FastAPI endpoints acting as the entry point, resolving dependencies.

## Consequences
- **Pros:** High testability, decoupled infrastructure, easier onboarding for complex business rules.
- **Cons:** Steeper learning curve initially, more boilerplate code (e.g., mapping between SQLAlchemy models and Domain entities).
