# Study Task Board - Vanilla JS Version

This is a browser-only CRUD app for tracking study tasks. It was generated and refined with Codex as the AI app generation assistant.

## Tech Stack

- HTML
- CSS
- Vanilla JavaScript
- Browser `localStorage` for persistence

## Features

- Create, read, update, and delete study tasks
- Mark tasks complete or reopen them
- Filter by all, open, and done
- Basic validation for task titles
- Persistent data in the browser

## Run Locally

No install step is required.

1. Open `index.html` in a browser.
2. Add, edit, complete, filter, and delete tasks.

Optional local server:

```bash
python3 -m http.server 5173
```

Then visit `http://localhost:5173/week5/taskflow-js/` from the repo root.

## Environment Configuration

None.

## Deviations, Known Issues, and Manual Fixes

- This version uses browser storage instead of a database because the stack is intentionally no-build and frontend-only.
- Data is scoped to the current browser and can be cleared by deleting site data.
- Manual refinements after AI generation included responsive layout, validation copy, and filter behavior.
