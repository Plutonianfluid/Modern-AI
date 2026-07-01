# Week 4 — The Autonomous Coding Agent IRL

This week, your task is to build at least **2 automations** for this repository using Codex.
The Codex automation options are:

- Codex skills or custom prompts for reusable workflows

- `AGENTS.md` files for repository or context guidance

- Codex subagents/custom agents (role-specialized agents working together)

- MCP servers integrated into Codex

Your automations should meaningfully improve a developer workflow - for example, by streamlining tests, documentation, refactors, or data-related tasks. You will then use the automations you create to expand upon the starter application found in `week4/`.

These are some resources you can read to understand Codex more and its automation options:

1. **Codex docs:** [developers.openai.com/codex](https://developers.openai.com/codex)

2. **AGENTS.md guidance:** [agents.md](https://agents.md)

## Explore the Starter Application
Minimal full‑stack starter application designed to be a **"developer's command center"**. 
- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Tasks to practice agent-driven workflows

Use this application as your playground to experiment with the Codex automations you build.

### Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent-driven workflows
```

### Quickstart

1) Activate your conda environment.

```bash
conda activate moderndev
```

2) Run the app (from `week4/` directory)

```bash
make run
```

3) Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

4) Play around with the starter application to get a feel for its current features and functionality.


### Testing
Run the tests (from `week4/` directory)
```bash
make test
```

### Formatting/Linting
```bash
make format
make lint
```

## Part I: Build Your Automation (Choose 2 or more)
Now that you’re familiar with the starter application, your next step is to build automations to enhance or extend it. Below are several automation options you can choose from. You can mix and match across categories.

As you build your automations, document your changes in the `writeup.md` file. Leave the *"How you used the automation to enhance the starter application"* section empty for now - you will be returning to this in Part II of the assignment.

### A) Codex skills or custom prompts
Codex skills and custom prompts are features for repeated workflows. Skills are preferred for reusable, shareable task behavior; custom prompts can expose local reusable prompts through `/prompts:name`.


- Example 1: Test runner with coverage
  - Name: `tests.md`
  - Intent: Run `pytest -q backend/tests --maxfail=1 -x` and, if green, run coverage.
  - Inputs: Optional marker or path.
  - Output: Summarize failures and suggest next steps.
- Example 2: Docs sync
  - Name: `docs-sync.md`
  - Intent: Read `/openapi.json`, update `docs/API.md`, and list route deltas.
  - Output: Diff-like summary and TODOs.
- Example 3: Refactor harness
  - Name: `refactor-module.md`
  - Intent: Rename a module (e.g., `services/extract.py` → `services/parser.py`), update imports, run lint/tests.
  - Output: A checklist of modified files and verification steps.

>*Tips: Keep workflows focused, use arguments where appropriate, and prefer idempotent steps. Consider allowlisting safe tools and using non-interactive mode for repeatability.*

### B) `AGENTS.md` guidance files
Codex reads `AGENTS.md` files when starting a session, allowing you to provide repository-specific instructions, context, or guidance that influence Codex's behavior. Create an `AGENTS.md` in the repo root (and optionally in `week4/` subfolders) to guide Codex's behavior.

- Example 1: Code navigation and entry points
  - Include: How to run the app, where routers live (`backend/app/routers`), where tests live, how the DB is seeded.
- Example 2: Style and safety guardrails
  - Include: Tooling expectations (black/ruff), safe commands to run, commands to avoid, and lint/test gates.
- Example 3: Workflow snippets
  - Include: “When asked to add an endpoint, first write a failing test, then implement, then run pre-commit.”

> *Tips: Iterate on `AGENTS.md` like a prompt, keep it concise and actionable, and document custom tools/scripts you expect Codex to use.*

### C) Codex subagents/custom agents (role-specialized)

Subagents/custom agents are specialized AI assistants configured to handle specific tasks with their own system prompts, tools, and context. Design two or more cooperating agents, each responsible for a distinct step in a single workflow.

- Example 1: TestAgent + CodeAgent
  - Flow: TestAgent writes/updates tests for a change → CodeAgent implements code to pass tests → TestAgent verifies.
- Example 2: DocsAgent + CodeAgent
  - Flow: CodeAgent adds a new API route → DocsAgent updates `API.md` and `TASKS.md` and checks drift against `/openapi.json`.
- Example 3: DBAgent + RefactorAgent
  - Flow: DBAgent proposes a schema change (adjust `data/seed.sql`) → RefactorAgent updates models/schemas/routers and fixes lints.

>*Tips: Use checklists/scratchpads, reset context (`/clear`) between roles, and run agents in parallel for independent tasks.*

## Part II: Put Your Automations to Work 
Now that you’ve built 2+ automations, let's put them to use! In the `writeup.md` under section *"How you used the automation to enhance the starter application"*, describe how you leveraged each automation to improve or extend the app’s functionality.

e.g. If you implemented the custom slash command `/generate-test-cases`, explain how you used it to interact with and test the starter application.


## Deliverables
1) Two or more automations, which may include:
  - Codex skills or custom prompts
  - `AGENTS.md` files
  - Codex subagent/custom agent prompts/configuration (documented clearly, files/scripts if any)
  - MCP server configuration for Codex, if used

2) A write-up `writeup.md` under `week4/` that includes:
  - Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
  - Design of each automation, including goals, inputs/outputs, steps
  - How to run it (exact commands), expected outputs, and rollback/safety notes
  - Before vs. after (i.e. manual workflow vs. automated workflow)
  - How you used the automation to enhance the starter application