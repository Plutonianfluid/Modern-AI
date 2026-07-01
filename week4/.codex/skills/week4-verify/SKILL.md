---
name: week4-verify
description: Use this skill when working in the week4 FastAPI starter app to verify changes, summarize test results, and produce assignment-ready notes about what changed.
---

# Week 4 Verify

<!-- Codex assignment change: this file is Automation #2. It defines a reusable Codex workflow for checking this repo after a change. -->

Use this workflow after making a small app change in the Week 4 starter repo.

## Steps

1. Inspect the relevant changed files with `git diff`.
2. Run `make test` from the `week4/` directory.
3. If tests fail, summarize the first failing test, the likely cause, and the next fix.
4. If tests pass, summarize:
   - files changed
   - user-visible behavior changed
   - tests or checks run
   - any remaining risk
5. When updating the assignment writeup, keep the explanation concrete and tied to the actual files changed.

## Safety

- Do not run destructive Git commands.
- Do not modify `data/app.db` for verification.
- If the environment lacks dependencies, report the missing command/package instead of inventing a passing result.
