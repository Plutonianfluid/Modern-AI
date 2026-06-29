# Modern AI Assignments

This repository contains course assignments for building AI-assisted software systems with Python. The Week 2 project is an Action Item Extractor: a FastAPI and SQLite app that turns free-form notes into saved action items through a small web interface and API.

## Project Structure

```text
modern-ai/
|-- week1/
|   `-- Prompting and tool-calling exercises
|-- week2/
|   |-- app/
|   |   |-- main.py              # FastAPI application setup
|   |   |-- db.py                # SQLite connection and persistence helpers
|   |   |-- schemas.py           # Pydantic request and response models
|   |   |-- routers/
|   |   |   |-- action_items.py  # Action item API routes
|   |   |   `-- notes.py         # Notes API routes
|   |   `-- services/
|   |       `-- extract.py       # Action item extraction logic
|   |-- frontend/
|   |   `-- index.html           # Minimal browser UI
|   |-- tests/
|   |   `-- test_extract.py      # Extraction unit tests
|   |-- assignment.md
|   `-- writeup.md
`-- pyproject.toml               # Poetry dependencies and tooling config
```

## Setup

These steps assume Python 3.12.

1. Install Anaconda.

2. Create and activate the course environment:

   ```bash
   conda create -n moderndev python=3.12 -y
   conda activate moderndev
   ```

3. Install Poetry:

   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. Install project dependencies from the repository root:

   ```bash
   poetry install --no-interaction
   ```

5. Optional: install and run Ollama if you want to use the LLM-powered extractor.

   ```bash
   ollama run llama3.1
   ```

## Running The Week 2 App

From the repository root, start the FastAPI server:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Open the frontend in your browser:

```text
http://127.0.0.1:8000/
```

The page lets you paste notes, extract action items, optionally save the source note, mark action items as done, run the LLM extraction endpoint, and list saved notes.

## Week 2 API

The FastAPI app is defined in `week2/app/main.py`. It initializes the SQLite database on startup, serves the HTML frontend at `/`, and includes routes for notes and action items.

### Frontend

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Serves `week2/frontend/index.html`. |

### Notes

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/notes` | Creates a saved note. |
| `GET` | `/notes` | Lists all saved notes, newest first. |
| `GET` | `/notes/{note_id}` | Retrieves one saved note by ID. |

Example note request:

```json
{
  "content": "Meeting notes go here"
}
```

Example note response:

```json
{
  "id": 1,
  "content": "Meeting notes go here",
  "created_at": "2026-06-27 12:00:00"
}
```

### Action Items

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/action-items/extract` | Extracts action items from notes and saves the generated items. |
| `POST` | `/action-items/extract-llm` | Extracts action items through the LLM extractor when available. |
| `GET` | `/action-items` | Lists saved action items. Accepts optional `note_id` query parameter. |
| `POST` | `/action-items/{action_item_id}/done` | Marks an action item as done or not done. |

Example extraction request:

```json
{
  "text": "- Write tests\n- Update documentation",
  "save_note": true
}
```

Example extraction response:

```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "text": "Write tests"
    },
    {
      "id": 2,
      "text": "Update documentation"
    }
  ]
}
```

Example mark-done request:

```json
{
  "done": true
}
```

Example mark-done response:

```json
{
  "id": 1,
  "done": true
}
```

## Database

Week 2 uses SQLite. The database is created automatically at:

```text
week2/data/app.db
```

The app creates two tables:

- `notes`: stores the original note text and creation time.
- `action_items`: stores extracted task text, completion state, creation time, and optional note linkage.

Database access is centralized in `week2/app/db.py`.

## Running Tests

Run all tests:

```bash
poetry run pytest
```

Run only Week 2 tests:

```bash
poetry run pytest week2/tests
```

Run the extractor test file directly:

```bash
poetry run pytest week2/tests/test_extract.py
```

If a test calls an Ollama-backed extractor, make sure Ollama is installed, running, and has the configured model available.

## Development Checks

Run Ruff against the Week 2 backend:

```bash
poetry run ruff check week2/app
```

Run Python compile checks:

```bash
poetry run python -m compileall week2/app week2/frontend
```

## Main Dependencies

- FastAPI for the backend API.
- Uvicorn for the local development server.
- SQLite for local persistence.
- Pydantic for request and response schemas.
- Pytest for tests.
- Ollama for local LLM-backed extraction.
