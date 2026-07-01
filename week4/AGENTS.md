# Week 4 Codex Guidance

<!-- Codex assignment change: this file is Automation #1. Codex reads AGENTS.md as persistent repo guidance before working in this project. -->

## Project Map

- FastAPI app entry point: `backend/app/main.py`
- API routers: `backend/app/routers/`
- SQLAlchemy models: `backend/app/models.py`
- Pydantic schemas: `backend/app/schemas.py`
- Static frontend: `frontend/`
- Tests: `backend/tests/`
- Seed data and SQLite database: `data/`

## Commands

- Run the app from `week4/`: `make run`
- Run tests from `week4/`: `make test`
- Format code from `week4/`: `make format`
- Lint code from `week4/`: `make lint`

## Workflow Rules

- Prefer small, testable changes that match the existing FastAPI and static frontend patterns.
- When changing backend behavior, add or update focused tests in `backend/tests/`.
- When changing API routes, check whether frontend code or docs need to be updated too.
- Before reporting that work is complete, run `make test` when the Python environment has the required packages.
- Do not remove seed data or reset `data/app.db` unless the user explicitly asks.
