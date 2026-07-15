# Warp Drive Prompt: Verify a Week 6 Task

Inputs: `task_number` and optional `test_path`.

```text
You are validating Week 6 task {{task_number}}. Work only inside week6/. First read
docs/TASKS.md and inspect the current diff. Run automations/verify-week6.sh
{{test_path}}. If a check fails, make the smallest in-scope correction and rerun the
checks. Summarize changed files, acceptance criteria verified, and any remaining risk.
Never commit, push, install dependencies, or alter another week without approval.
```

Save this as a Warp Drive prompt with `task_number` required and `test_path` optional.
The command is idempotent and accepts a focused pytest path for faster feedback.
