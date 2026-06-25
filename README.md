# Autonomous AI Recruiting Platform

An enterprise-grade, production-ready Multi-Agent Operating System explicitly configured for fully autonomous recruiting workflows.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Release_Candidate-orange.svg)

## Overview
This repository contains a full-stack Next.js and Python application demonstrating an advanced, deeply decoupled AI architecture. 

It proves out a foundational architecture where massive swarms of LLM-backed agents can securely execute complex organizational goals—like parsing resumes, evaluating skills, running semantic search, coordinating calendars, and drafting candidate emails—without ever interacting with the underlying infrastructure directly.

## Architecture Highlights
- **Hexagonal / Clean Architecture:** Application and Domain logic are 100% agnostic to the infrastructure layer.
- **Organization Plugins:** The Recruiting features are injected as a plugin. The underlying Agent Runtime and Coordination platforms can be perfectly reused to build an AI Sales or AI Customer Support organization.
- **Zero-Trust Tool Execution:** Agents operate within a strict `ExecutionBudget` enforced by an `OrganizationPolicyEngine`.
- **Time-Travel Debugging:** The `ReplayEngine` captures `SessionSnapshots` across the `CognitivePipeline`, allowing developers to step through historic agent reasoning traces.
- **Distributed Coordination:** Agents never call each other. They communicate asynchronously via an `AgentCommunicationBus` enabling horizontal scale.

## Getting Started
We provide a comprehensive `Makefile` to manage the developer experience.

```bash
# Install dependencies
make setup

# Run the platform (Docker Compose)
make dev

# Run test suites
make test
```

## Documentation
Please refer to the `/docs` directory for deep-dive architectural overviews:
- `docs/platform-overview.md`
- `docs/architecture-book.md`
- `docs/ENGINEERING_DECISIONS.md`
- `docs/reports/` (Security, Observability, Release Validations)

## License
MIT License.
