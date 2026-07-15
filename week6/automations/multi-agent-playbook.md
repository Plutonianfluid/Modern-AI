# Warp Multi-Agent Playbook

Use separate Warp tabs and isolated worktrees so concurrent agents do not overwrite files.

1. Coordinator creates branches/worktrees named `week6-notes`, `week6-actions`, and
   `week6-tests-docs`.
2. Notes agent owns tasks 2 and 3: notes schemas/router, notes UI, and notes tests.
3. Actions agent owns tasks 4 and 8: action-item router/UI and action-item tests.
4. Verification agent owns task 10 and automation documentation. It reviews tests but
   does not edit files currently owned by another agent.
5. Each agent runs `automations/verify-week6.sh` and reports its commit plus check output.
6. Coordinator integrates notes, then actions, then tests/docs; resolves shared frontend
   changes deliberately; reruns the full verification script; and reviews `git diff`.

Agents may read and edit only `week6/` and run local checks. Dependency installation,
Git history changes, network access, commits, and pushes require explicit supervision.
