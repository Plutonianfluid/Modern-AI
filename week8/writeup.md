# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Submission Details

Name: **Evan** \
This assignment took me about **5** hours to do.


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> [Graphite PR #1](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/1) ·
> [GitHub PR #1](https://github.com/Plutonianfluid/Modern-AI/pull/1) ·
> [commit `928eb87`](https://github.com/Plutonianfluid/Modern-AI/commit/928eb878d0e15e3c9f1df9960b3fd65eb0a04a6f)

b. PR Description
> Added read and delete endpoints for action items, a delete endpoint for notes,
> and consistent 404 responses for missing records. Request models now reject empty
> required fields and invalid project IDs. Pagination parameters have explicit
> lower and upper bounds, while sorting uses an allowlist instead of accepting
> arbitrary model attributes. Testing: `poetry run pytest -q backend/tests`
> (7 passed at this stack layer) and `poetry run ruff check .` (passed).

c. Graphite Diamond generated code review
> Graphite completed its review of
> [PR #1](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/1) and
> reported **“Graphite found no issues.”** It left no inline comments, so no
> Graphite-requested changes were needed.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> [Graphite PR #2](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/2) ·
> [GitHub PR #2](https://github.com/Plutonianfluid/Modern-AI/pull/2) ·
> [commit `ec73a09`](https://github.com/Plutonianfluid/Modern-AI/commit/ec73a09a4b273cf76b0283fb6479549041791a86)

b. PR Description
> Expanded deterministic extraction to recognize TODO, ACTION, ACTION ITEM, and
> NEXT STEP prefixes; unchecked Markdown task boxes; common imperative verbs; and
> exclamation-mark actions. Prefixes and bullet syntax are removed from returned
> text, completed checkboxes are ignored, blank input is supported, and duplicate
> items are removed case-insensitively while preserving order. Tests cover the
> original cases plus checkboxes, imperative language, deduplication, completed
> items, background text, and empty input. The stack passes 9 tests at this layer.

c. Graphite Diamond generated code review
> Graphite completed its review of
> [PR #2](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/2) and
> reported **“Graphite found no issues.”** It left no inline comments, so no
> Graphite-requested changes were needed.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> [Graphite PR #3](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/3) ·
> [GitHub PR #3](https://github.com/Plutonianfluid/Modern-AI/pull/3) ·
> [commit `e64fa7b`](https://github.com/Plutonianfluid/Modern-AI/commit/e64fa7bdc8cbfd11587f923bcea0a3fc14e05803)

b. PR Description
> Added a `Project` model and a one-to-many relationship from projects to action
> items through an optional foreign key. Added create/list/get project endpoints,
> duplicate-name conflict handling, project assignment on action-item creation and
> patching, and project filtering on the action-item list. The relationship remains
> optional so existing action items and clients stay compatible. Tests cover
> creation, assignment, filtering, unassignment, alphabetical listing, duplicate
> names, validation, and missing projects.
> The stack passes 11 tests at this layer.

c. Graphite Diamond generated code review
> Graphite completed its review of
> [PR #3](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/3) and
> reported **“Graphite found no issues.”** It left no inline comments, including
> none about relationship lifecycle behavior or database migrations.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> [Graphite PR #4](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/4) ·
> [GitHub PR #4](https://github.com/Plutonianfluid/Modern-AI/pull/4) ·
> [commit `4edeec2`](https://github.com/Plutonianfluid/Modern-AI/commit/4edeec20766436d2b7289b50ea9c8720298693b9)

b. PR Description
> Added coverage for ascending and descending sorting, page boundaries using
> `skip` and `limit`, completed/project filters, deterministic ordering, and invalid
> pagination or sort values. The API now adds `id` as a stable secondary sort key,
> preventing records with equal primary sort values from moving between pages.
> The complete backend suite passes with 13 tests.

c. Graphite Diamond generated code review
> Graphite completed its review of
> [PR #4](https://app.graphite.com/github/pr/Plutonianfluid/Modern-AI/4) and
> reported **“Graphite found no issues.”** It left no inline comments, so no
> Graphite-requested changes were needed.

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> My manual review focused mainly on correctness and API shape: status codes for
> missing resources, validation boundaries, stable pagination, foreign-key checks,
> backward compatibility, and whether tests exercised both success and failure
> paths. I also reviewed naming and readability in the extraction patterns. I
> deliberately checked that completed Markdown boxes were not treated as new work
> and that repeated extracted actions did not create duplicates.

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> Graphite reported no issues on all four PRs, while my manual review produced
> concrete observations for every task. For Task 1, I found that permissive
> `hasattr` sorting silently accepted bad input, so I changed it to an explicit
> allowlist and a 422 response. For Task 2, I checked false positives, completed
> checkboxes, duplicate actions, and preservation of input order. For Task 3, I
> checked missing project IDs, nullable assignment, duplicate names, and backward
> compatibility. For Task 4, I checked page boundaries, stable ordering when sort
> values match, combined filters, and invalid parameters. Graphite provided useful
> independent confirmation but no additional comments to accept, reject, or mark
> as duplicates.

c. When the AI reviews were better/worse than yours (cite specific examples)
> The AI reviews were faster and useful as a clean second opinion, but the manual
> review was more informative in this stack because Graphite left no comments. A
> specific example is Task 1: my review identified both silently accepted invalid
> sort fields and unstable ordering when records shared the same sort value.
> Graphite reported no issues on that PR. Likewise, Graphite did not mention Task
> 3's lack of a migration for an existing database or the need to define project
> deletion behavior. Graphite was not wrong—tests and linting passed—but it did not
> add findings beyond the manual review.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> I am comfortable using AI review as a second reviewer, but not as the approval
> authority. I would rely on it for broad scans, repetitive error handling, naming,
> and missing-test suggestions. I would require manual review for schema changes,
> data deletion, security boundaries, concurrency, migrations, and business rules
> the model cannot infer. My heuristic is to verify every correctness or security
> claim with a test or primary documentation, treat stylistic comments as optional,
> and never merge solely because the AI reported no issues.
