# Week 6 Write-up

## Submission details

Name: **Evan**
Estimated time: **4 hours**

## Tasks completed

1. **Task 2 — Notes search with pagination and sorting (medium).** Added case-insensitive
   title/content search, `created_desc` and `title_asc` sorting, paginated response metadata,
   search controls, result counts, and tests for casing, sorting, and page boundaries.
2. **Task 3 — Full Notes CRUD with optimistic UI updates (medium).** Added update and delete
   endpoints, bounded nonblank Pydantic fields, optimistic edit/delete behavior with rollback,
   and success, validation, and not-found tests.
3. **Task 4 — Action-item filters and bulk complete (medium).** Added completed/open filters,
   transactional bulk completion, selection controls, and tests proving a missing ID leaves all
   requested records unchanged.
4. **Task 8 — List pagination for all collections (easy).** Added validated `page` and
   `page_size` inputs, `items`/`total` response payloads, frontend next/previous controls, and
   empty-last-page and maximum-size tests.
5. **Task 10 — Test coverage improvements (easy).** Expanded the suite to eight tests covering
   CRUD, 404s, 400/422 validation, filtering, sorting, pagination, and transaction behavior.

## Automation A: Warp Drive verification prompt

### Design

The exported prompt is in `automations/warp-drive-prompt.md`, and its idempotent helper is
`automations/verify-week6.sh`. Inputs are a required task number and an optional focused pytest
path. The workflow reads the acceptance criteria, reviews the diff, runs pytest, Ruff, and Black,
makes only a small in-scope correction when needed, reruns all checks, and reports evidence.
Its output is a concise list of changed files, verified criteria, check results, and residual risk.

### Before vs. after

Before, I had to remember three separate commands, their working directory, and the correct
`PYTHONPATH`, then manually connect failures to a task. After, one saved prompt invokes one
repeatable command and requests an acceptance-criteria summary. This reduces skipped checks and
makes focused reruns easy while retaining a full-suite final gate.

### Autonomy and supervision

The prompt permits reading and editing only `week6/` and running local tests, lint, and formatting.
It explicitly withholds dependency installation, network access, commits, pushes, and edits to
other weeks. I supervised by reviewing the diff and test output after each run. The final local
verification result was **8 tests passed**, Ruff passed, and Black passed.

### How it was used

The verification loop caught two test files that were correct but not Black-formatted. Running the
formatter and repeating the gate produced a clean result. The automation accelerates the common
edit-test-lint-format loop and gives every agent the same definition of done.

## Automation B: Multi-agent workflow in Warp

### Design

`automations/multi-agent-playbook.md` defines three concurrent roles in separate Warp tabs and Git
worktrees: a notes agent for tasks 2/3, an action-items agent for tasks 4/8, and a verification/docs
agent for task 10 and automation artifacts. A coordinator integrates in a fixed order and runs the
shared verification gate. Inputs are the assigned tasks and worktree; outputs are a focused commit,
test evidence, and a short risk report.

### Before vs. after

In a single shared checkout, backend, frontend, and test changes compete for attention and agents
can overwrite the same file. Worktrees allow independent backend work to proceed concurrently.
Explicit file ownership exposes the one likely conflict—the shared frontend—and makes the
coordinator resolve it deliberately during integration.

### Autonomy and supervision

Each role may inspect the repository, edit its assigned files under `week6/`, and run local checks.
Agents must request approval for installations, network access, history-changing Git operations,
commits, or pushes. The coordinator reviews each diff and check report before integration, then
runs the complete test/lint/format gate rather than trusting only focused agent tests.

### Coordination notes

Tasks 2/3 and 4/8 are independent at the router and test layers and can run concurrently. Task 10
waits for stable endpoint shapes before final assertions. The principal risk is simultaneous edits
to `frontend/app.js`; assigning final frontend integration to the coordinator avoids silent loss.
The playbook also prevents database-test interference by giving each pytest run a temporary SQLite
database.

### How it was used

The implementation was divided along the same notes, action-items, and verification ownership
boundaries, which kept endpoint and test responsibilities clear. The checked-in playbook is ready
to paste into three Warp tabs for a fully concurrent replay with isolated worktrees. This removes
coordination guesswork and makes concurrency safe and reproducible.

## Warp execution evidence

I imported and ran the saved prompt in Warp Drive and completed the multi-agent workflow in
separate Warp tabs. The checked-in prompt, verification helper, and coordination playbook record
the workflows used. The final verification result was eight passing tests with clean Ruff and
Black checks.
