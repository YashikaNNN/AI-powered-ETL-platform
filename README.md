# AI ETL Analytics Platform

Monorepo for an AI-powered ETL analytics platform.

## Stack

| Layer      | Technology                          |
| ---------- | ----------------------------------- |
| Frontend   | Next.js (App Router)                |
| Backend    | FastAPI                             |
| Database   | PostgreSQL                          |
| ETL        | Python pipelines                    |
| AI         | Google Gemini API                   |

## Repository layout

```
frontend/     Next.js UI and API client
backend/      FastAPI REST API
etl/          Extract, transform, load jobs
infrastructure/   Postgres init scripts, Docker
scripts/      Dev and ops helpers
```

## Quick start

1. Copy environment files: `cp .env.example .env` and fill in secrets.
2. Start PostgreSQL: `docker compose up -d postgres`
3. Backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
4. Frontend: `cd frontend && npm install && npm run dev`
5. ETL: `cd etl && pip install -r requirements.txt && cd .. && PYTHONPATH=. python -m etl.jobs.run_pipeline`

## Architecture

- **Routes** — HTTP handlers (FastAPI routers, Next.js API routes if needed)
- **Services** — Business logic and orchestration
- **Models** — ORM entities and domain types
- **ETL layers** — Extract → Transform → Load with clear boundaries
- **Utilities** — Shared helpers (logging, config, clients)
