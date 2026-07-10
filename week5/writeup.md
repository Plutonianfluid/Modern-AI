# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Submission Details

Name: **Evan** \
This assignment took me about **4** hours to do.


## App Concept 
Study Task Board is a small CRUD app for managing coursework tasks. Users can add a task with a title, course area, priority, and notes; view all saved tasks; edit task details; mark tasks complete or reopen them; and delete tasks. The goal is to provide the same core workflow in two different stacks while keeping the app simple enough to run locally.


## Version #1 Description
APP DETAILS:
===============
Folder name: `taskflow-js`
AI app generation platform: Codex was used as the AI generation assistant for this local version.
Tech Stack: HTML, CSS, Vanilla JavaScript
Persistence: Browser `localStorage`
Frameworks/Libraries Used: None
(Optional but recommended) Screenshots of core flows: `Screenshots/js-add-task.png`

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The main limitation of the browser-only stack is that persistence is local to one browser. I used `localStorage` so the app still has create/read/update/delete behavior without requiring a server or install step. I also added validation and empty states so the UI handles common user mistakes clearly.

b. Prompting (e.g. what required additional guidance; what worked poorly/well): The most useful guidance was to specify the resource model up front: title, category, priority, notes, and done status. The prompt also needed to ask for complete CRUD flows instead of only a visual prototype.

c. Approximate time-to-first-run and time-to-feature metrics: Time-to-first-run was about 5 minutes because the app has no dependency install. Time-to-feature-complete was about 45 minutes including styling, validation, filtering, and README notes.

## Version #2 Description
APP DETAILS:
===============
Folder name: `taskflow-fastapi`
AI app generation platform: Codex was used to generate and refine the implementation.
Tech Stack: Python FastAPI backend, SQLite database, Vanilla JavaScript frontend
Persistence: SQLite database file created automatically as `tasks.db`
Frameworks/Libraries Used: FastAPI, Pydantic, Uvicorn, SQLite
(Optional but recommended) Screenshots of core flows: `Screenshots/fastapi-main.png`

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: The API version needed more structure than the frontend-only version because the UI, REST endpoints, validation, and database all had to agree on the same task shape. I resolved that by defining a Pydantic model, using SQLite constraints, and keeping the frontend API calls small and consistent.

b. Prompting (e.g. what required additional guidance; what worked poorly/well): Prompting worked best when it included both the user-facing flows and the backend contract. Asking for "CRUD with persistence" alone was not specific enough; naming the exact fields and routes made the generated app more complete.

c. Approximate time-to-first-run and time-to-feature metrics: Time-to-first-run was about 15 minutes with dependencies already available. Time-to-feature-complete was about 75 minutes including database setup, API routes, frontend integration, error handling, and documentation.

## Overall Reflection
How does using a specialized AI app generation platform like bolt feel compared to general AI agents like Claude Code?

Specialized app generators like Bolt feel faster for getting a polished first screen because they are optimized for turning a product description into a working prototype. A coding agent like Codex or Claude Code feels more flexible once the project has constraints, bugs, or existing files because it can inspect the repo.
