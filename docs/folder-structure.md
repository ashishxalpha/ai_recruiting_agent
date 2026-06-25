# Folder Structure

```text
.
├── backend/
│   ├── src/
│   │   ├── domain/
│   │   │   ├── entities.py
│   │   │   ├── enums.py
│   │   │   └── interfaces/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   │   ├── database/
│   │   │   │   ├── models.py
│   │   │   │   ├── base.py
│   │   │   │   └── repositories/
│   │   │   └── providers/
│   │   │       └── storage/
│   │   ├── presentation/
│   │   ├── observability/
│   │   │   ├── logging.py
│   │   │   ├── tracing.py
│   │   │   └── metrics.py
│   │   ├── core/
│   │   └── main.py
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   ├── types/
│   ├── lib/
│   ├── package.json
│   ├── Dockerfile
│   └── Dockerfile.dev
├── docs/
│   ├── decisions/
│   │   ├── 0001-use-domain-driven-design.md
│   │   ├── 0002-asynchronous-resume-processing.md
│   │   ├── ADR-003-storage-provider.md
│   │   ├── ADR-004-background-job-architecture.md
│   │   └── ADR-005-database-design.md
│   ├── architecture.md
│   ├── folder-structure.md
│   ├── database-schema.md
│   ├── domain-model.md
│   ├── api-reference.md
│   └── implementation-log.md
└── docker-compose.yml
```
