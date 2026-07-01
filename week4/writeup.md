# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> I used Codex's `AGENTS.md` guidance pattern as the inspiration. The goal was to give Codex stable repository context before each task, similar to how the original assignment described persistent agent guidance files.

b. Design of each automation, including goals, inputs/outputs, steps
> Automation: `AGENTS.md`.
> Goal: make Codex consistently understand the Week 4 repo layout, commands, and safety expectations.
> Inputs: any future Codex request made from this repo.
> Outputs: more consistent Codex behavior, especially around where to edit files and what commands to run.
> Steps: Codex reads the file, uses the project map to find backend/frontend/tests, follows the workflow rules, and runs the recommended checks when possible.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> Run it by starting Codex in the `week4/` repo; Codex automatically reads `AGENTS.md`.
> Expected output: Codex should know that the app runs with `make run`, tests run with `make test`, backend routes live in `backend/app/routers/`, and frontend files live in `frontend/`.
> Rollback/safety: review `git diff`; if the guidance causes confusion, edit or remove `AGENTS.md`.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> Before: I had to restate the project structure, commands, and safety rules in each prompt.
> After: Codex has that context loaded as reusable project guidance.

e. How you used the automation to enhance the starter application
> I used the `AGENTS.md` guidance while implementing the note search improvement. It directed the work toward the correct files: `backend/app/routers/notes.py`, `frontend/app.js`, `frontend/index.html`, and `backend/tests/test_notes.py`.


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> I used Codex skills as the inspiration because they provide reusable task workflows. This skill is focused on verifying changes in the Week 4 starter app.

b. Design of each automation, including goals, inputs/outputs, steps
> Automation: `.codex/skills/week4-verify/SKILL.md`.
> Goal: provide a repeatable verification workflow after app changes.
> Inputs: a completed or in-progress code change.
> Outputs: a summary of changed files, test results, user-visible behavior, and remaining risks.
> Steps: inspect `git diff`, run `make test`, summarize failures or passing results, and connect the result back to the assignment writeup.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> Run it by asking Codex to use the `week4-verify` skill after a change, for example: "Use the week4-verify skill to check this change."
> Expected output: Codex reports the files changed, whether `make test` passed, and what the change does.
> Rollback/safety: the skill explicitly avoids destructive Git commands and avoids modifying `data/app.db` during verification.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> Before: I had to manually remember to inspect the diff, run tests, and summarize results.
> After: the verification checklist is captured in a reusable Codex skill.

e. How you used the automation to enhance the starter application
> I used the verification workflow to summarize what changed after the search update and to catch problems in the implementation. The skill guided Codex to inspect the diff and test changes into one explanation, and verify the work with `make test`.


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Not used. I completed the assignment with two automations: `AGENTS.md` and the `week4-verify` Codex skill.

b. Design of each automation, including goals, inputs/outputs, steps
> Not applicable.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> Not applicable.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> Not applicable.

e. How you used the automation to enhance the starter application
> Not applicable.
