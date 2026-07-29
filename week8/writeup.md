# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Submission Details

Name: **Evan** \
This assignment took me about **5** hours to do.


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> Local implementation: `backend/app/routers/notes.py`,
> `backend/app/routers/action_items.py`, and `backend/app/schemas.py`.
> A hosted commit/issue link will be added when the four task branches are pushed.

b. PR Description
> Added read and delete endpoints for action items, a delete endpoint for notes,
> and consistent 404 responses for missing records. Request models now reject empty
> required fields and invalid project IDs. Pagination parameters have explicit
> lower and upper bounds, while sorting uses an allowlist instead of accepting
> arbitrary model attributes. Testing: `poetry run pytest -q backend/tests`
> (11 passed) and `poetry run ruff check week8` (passed).

c. Graphite Diamond generated code review
> Pending external review. Graphite Diamond can only produce its review after this
> task is pushed as a PR; no Graphite review or comment link was fabricated here.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> Local implementation: `backend/app/services/extract.py` and
> `backend/tests/test_extract.py`. A hosted commit/issue link will be added after
> the task branch is pushed.

b. PR Description
> Expanded deterministic extraction to recognize TODO, ACTION, ACTION ITEM, and
> NEXT STEP prefixes; unchecked Markdown task boxes; common imperative verbs; and
> exclamation-mark actions. Prefixes and bullet syntax are removed from returned
> text, completed checkboxes are ignored, blank input is supported, and duplicate
> items are removed case-insensitively while preserving order. Tests cover the
> original cases plus checkboxes, imperative language, deduplication, completed
> items, background text, and empty input.

c. Graphite Diamond generated code review
> Pending external review. This section should be updated with the Graphite comment
> link and disposition once the extraction PR exists.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> Local implementation: `backend/app/models.py`,
> `backend/app/routers/projects.py`, and related schema/router changes. A hosted
> commit/issue link will be added after the task branch is pushed.

b. PR Description
> Added a `Project` model and a one-to-many relationship from projects to action
> items through an optional foreign key. Added create/list/get project endpoints,
> duplicate-name conflict handling, project assignment on action-item creation and
> patching, and project filtering on the action-item list. The relationship remains
> optional so existing action items and clients stay compatible. Tests cover
> creation, assignment, filtering, unassignment, alphabetical listing, duplicate
> names, validation, and missing projects.

c. Graphite Diamond generated code review
> Pending external review. A useful focus for Graphite is relationship lifecycle
> behavior (especially deleting projects) and whether a migration is required for
> an already-deployed SQLite database.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> Local implementation: `backend/tests/test_notes.py`,
> `backend/tests/test_action_items.py`, and `backend/tests/test_projects.py`.
> A hosted commit/issue link will be added after the task branch is pushed.

b. PR Description
> Added coverage for ascending and descending sorting, page boundaries using
> `skip` and `limit`, completed/project filters, deterministic ordering, and invalid
> pagination or sort values. The API now adds `id` as a stable secondary sort key,
> preventing records with equal primary sort values from moving between pages.
> The complete backend suite passes with 11 tests.

c. Graphite Diamond generated code review
> Pending external review. The Graphite review link and any resulting changes
> should be recorded here after the test PR is opened.

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> My manual review focused mainly on correctness and API shape: status codes for
> missing resources, validation boundaries, stable pagination, foreign-key checks,
> backward compatibility, and whether tests exercised both success and failure
> paths. I also reviewed naming and readability in the extraction patterns. I
> deliberately checked that completed Markdown boxes were not treated as new work
> and that repeated extracted actions did not create duplicates.

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> A real comparison is not yet possible because Graphite reviews require hosted
> PRs and none were available in this local workspace. For Task 1, my manual review
> found that permissive `hasattr` sorting silently fell back on bad input; this was
> changed to an explicit allowlist and a 422 response. For Task 2, I focused on
> false positives and preservation of input order. For Task 3, I focused on missing
> project IDs, nullable assignment, and duplicate names. For Task 4, I focused on
> page boundaries, sort direction, filters, and invalid parameters. After Graphite
> runs, each of its comments should be compared against these observations and
> marked accepted, rejected, or duplicate.

c. When the AI reviews were better/worse than yours (cite specific examples)
> Graphite has not run, so claiming that it was better or worse would be
> unsupported. My strongest manual finding was the unstable/permissive sort
> behavior: invalid fields were silently accepted and equal values lacked a stable
> tie-breaker. Likely AI-review targets include the absence of a database migration
> for existing installations and the unspecified project-deletion policy. If
> Graphite identifies either, that would be a valuable systems-level comment; if it
> only restates validation already covered by tests, the manual review was more
> useful for this change.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> I am comfortable using AI review as a second reviewer, but not as the approval
> authority. I would rely on it for broad scans, repetitive error handling, naming,
> and missing-test suggestions. I would require manual review for schema changes,
> data deletion, security boundaries, concurrency, migrations, and business rules
> the model cannot infer. My heuristic is to verify every correctness or security
> claim with a test or primary documentation, treat stylistic comments as optional,
> and never merge solely because the AI reported no issues.

