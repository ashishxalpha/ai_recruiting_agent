# Technical Debt & Future Improvements

## Current Technical Debt
1. **Mocked Stubs in Infrastructure:** Due to sandbox constraints, several modules inside `src/infrastructure` (e.g. the LLM Planner, the Vector DB client) utilize stubbed implementations returning static JSON instead of calling live remote endpoints.
2. **Missing Schema Migrations:** While Alembic is configured, massive rapid iterations over the domain models means a thorough review of the actual schema mappings in `alembic/versions` is necessary prior to production deployment.
3. **Frontend Component Duplication:** The fast iterative nature of building the Next.js `Studio` UI resulted in some duplicated Tailwind layout blocks across the various domain dashboards (e.g. `/tools`, `/agents`, `/coordination`).

## Roadmap for v1.1
- Replace infrastructure stubs with official `langchain-core` / `openai` SDK integrations.
- Introduce `RedisWorkingMemoryStore` to supplement the `PostgresWorkingMemoryStore` for low-latency session caching.
- Expand `MCPToolProvider` to officially bridge remote server-sent events.
