# Study Task Board - FastAPI Version

This is the API-backed version of the same Study Task Board CRUD app.

## Tech Stack

- Python
- FastAPI
- SQLite
- Vanilla JavaScript frontend served from FastAPI

## Features

- Create, read, update, and delete study tasks through REST endpoints
- Mark tasks complete or reopen them
- SQLite persistence in `tasks.db`
- Pydantic validation and API error handling
- Responsive browser UI

## Run Locally

From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then visit `http://127.0.0.1:8000`.

If you already installed the root course dependencies with Poetry, you can also run:

```bash
poetry run uvicorn main:app --reload --port 8000
```

Run that command from inside `week5/taskflow-fastapi`.

## API Routes

- `GET /api/tasks`
- `POST /api/tasks`
- `PUT /api/tasks/{task_id}`
- `DELETE /api/tasks/{task_id}`

## Environment Configuration

None. The SQLite database is created automatically at `week5/taskflow-fastapi/tasks.db`.

## Deviations, Known Issues, and Manual Fixes

- Authentication is intentionally omitted because the assignment only requires CRUD, persistence, validation, and a functional UI.
- The SQLite file is local development data and does not need to be committed.
- Manual refinements after AI generation included SQLite initialization, API error messages, and UI consistency with the frontend-only version.
