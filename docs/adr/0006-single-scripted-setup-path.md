# ADR-0006: Single Scripted Setup Path

- **Status:** Accepted
- **Date:** 2026-11-18
- **Deciders:** Caleb Fuller

## Six-Line Decision

```text
Decision:     scripted setup (`./script/setup` + `requirements.lock`)
Context:      Single-process stateless FastAPI web service with an in-memory 300s TTL cache and external VirusTotal v3 API; no local database, queue, or multi-service stack; run by Windows/macOS/Linux developers, CI runners, and post-graduation maintainers.
Consequence:  Successor must install Python 3.12–3.14 (with `venv`) and Git before running `./script/setup` (or the equivalent PowerShell `.venv` commands in `README.md`).
Rejected:     containers (`Dockerfile` / `compose.yaml`), because the app has zero local stateful services (no Postgres/Redis) and maintaining a container image alongside native Python scripts adds image-build overhead and dual-path drift without solving a multi-service problem.
Evidence:     ran clean on fresh clone (`$env:TEMP\capstone-amnesia-test`) on 2026-11-18, 2 minutes 41 seconds (clone -> setup -> 69 tests -> live `/health` & `/scan`).