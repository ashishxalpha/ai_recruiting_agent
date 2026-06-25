# Autonomous AI Recruiting Platform

An enterprise-grade, production-ready Multi-Agent Operating System explicitly configured for fully autonomous recruiting workflows.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview
This repository contains a full-stack Next.js and Python application demonstrating an advanced, deeply decoupled AI architecture. 

It proves out a foundational architecture where massive swarms of LLM-backed agents can securely execute complex organizational goals—like parsing resumes, evaluating skills, running semantic search, coordinating calendars, and drafting candidate emails—without ever interacting with the underlying infrastructure directly.

## Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy, LangGraph (Workflow Engine), Alembic
- **Frontend:** Next.js (React), Tailwind CSS, Lucide Icons, Shadcn UI
- **Database:** PostgreSQL with pgvector for semantic search and embeddings
- **Caching & Jobs:** Redis
- **Containerization:** Docker & Docker Compose

## How to Run Locally

We provide a comprehensive `docker-compose.yml` that stands up the entire environment (Postgres, Redis, Backend API, and Frontend Next.js Server).

### Prerequisites
- Docker and Docker Compose installed
- Node.js (for local frontend development)
- Python 3.10+ (for local backend development)

### 1. Environment Configuration
Copy the sample environment file and populate it with your API keys:

```bash
cp .env.example .env
```
Ensure you have the required API keys (e.g., OpenAI/Anthropic) populated in your `.env` file.

### 2. Start the Platform
Run the following command to start all services using Docker Compose:

```bash
docker-compose up --build
```

This will start:
- **Backend API:** `http://localhost:8000`
- **Frontend App:** `http://localhost:3000`
- **Postgres Database:** `localhost:5432`
- **Redis:** `localhost:6379`

### 3. Developer Commands
A `Makefile` is included to manage common tasks if you prefer running things outside of Docker:

```bash
# Install dependencies
make setup

# Run the platform (Docker Compose)
make dev

# Run test suites
make test
```

## License
MIT License.
