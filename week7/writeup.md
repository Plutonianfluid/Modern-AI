# Week 7 Write-up

## Submission Details

Name: **Evan Wang**  
This assignment took me about **1** hour to do.

## Brief findings overview

I scanned `week7/` locally with Semgrep 1.170.1 using the `p/security-audit` and
`p/secrets` rule packs, with metrics disabled. The initial scan ran 146 rules on
19 files and reported three blocking SAST findings: use of `eval`, execution of a
subprocess with `shell=True`, and a dynamic URL passed to `urllib`. The secrets
rules reported no exposed secrets. I removed the three unnecessary debug routes
because none of them is part of the notes application's required functionality.

For SCA coverage, I also audited the exact pins in `requirements.txt` with
`pip-audit --no-deps --disable-pip`. It reported 33 known vulnerabilities across
six direct dependencies. A normal resolved audit could not run because the
provided old FastAPI and Pydantic pins conflict on a current Python runtime. I
did not treat any of the three Semgrep findings as false positives or ignore any
Semgrep finding. Dependency modernization is valid follow-up work, but it was
kept outside these three targeted Semgrep fixes to avoid an unrelated framework
migration.

After the changes, the same Semgrep scan reported zero findings. The Week 7 test
suite also passed: `4 passed`.

## Fix #1

### a. File and line(s)

`backend/app/routers/notes.py`, original lines 102–105 (the `/debug/eval` route).

### b. Rule/category Semgrep flagged

`python.lang.security.audit.eval-detected.eval-detected` (SAST/code injection).

### c. Brief risk description

The route passed the user-controlled `expr` query parameter directly to Python's
`eval`. An attacker could execute arbitrary Python code with the permissions of
the API process, potentially reading data, changing files, or taking over the
server.

### d. Your change (short code diff or explanation, AI coding tool usage)

I used Codex to triage the finding and remove the entire `/notes/debug/eval`
endpoint:

```diff
-@router.get("/debug/eval")
-def debug_eval(expr: str) -> dict[str, str]:
-    result = str(eval(expr))
-    return {"result": result}
```

I also added a regression assertion in `backend/tests/test_notes.py` that checks
the route is not registered.

### e. Why this mitigates the issue

Removing the unused debug endpoint eliminates both the untrusted input and the
`eval` execution sink. There is no remaining URL through which a client can ask
the application to evaluate Python code.

## Fix #2

### a. File and line(s)

`backend/app/routers/notes.py`, original lines 108–113 (the `/debug/run` route).

### b. Rule/category Semgrep flagged

`python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`
(SAST/OS command injection).

### c. Brief risk description

The route sent a user-controlled command to `subprocess.run` with `shell=True`.
Shell metacharacters could therefore be used to execute arbitrary operating
system commands as the API process.

### d. Your change (short code diff or explanation, AI coding tool usage)

With Codex, I removed the unused `/notes/debug/run` endpoint and its local
`subprocess` import instead of preserving a public command-execution feature:

```diff
-@router.get("/debug/run")
-def debug_run(cmd: str) -> dict[str, str]:
-    import subprocess
-    completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
-    return {"returncode": str(completed.returncode), ...}
```

The regression test also verifies that this route is no longer registered.

### e. Why this mitigates the issue

The API no longer starts a shell or subprocess from client input, so shell
metacharacters and attacker-supplied commands cannot reach an OS command sink.

## Fix #3

### a. File and line(s)

`backend/app/routers/notes.py`, original lines 116–122 (the `/debug/fetch` route).

### b. Rule/category Semgrep flagged

`python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected`
(SAST/server-side request forgery and local file access).

### c. Brief risk description

The route passed an attacker-controlled URL to `urlopen`. An attacker could make
the server request internal services or use supported schemes such as `file://`
to read local resources that are not normally exposed by the web application.

### d. Your change (short code diff or explanation, AI coding tool usage)

I used Codex to remove the unused `/notes/debug/fetch` endpoint and its dynamic
`urlopen` call:

```diff
-@router.get("/debug/fetch")
-def debug_fetch(url: str) -> dict[str, str]:
-    from urllib.request import urlopen
-    with urlopen(url) as res:
-        body = res.read(1024).decode(errors="ignore")
-    return {"snippet": body}
```

The new regression test verifies that this route is absent as well.

### e. Why this mitigates the issue

Clients can no longer make the server fetch arbitrary URLs. Removing the feature
fully closes the SSRF and `file://` access path, including redirect and DNS
rebinding edge cases that a partial URL check might miss.
