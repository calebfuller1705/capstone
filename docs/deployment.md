# Deployment Guide — Phishing URL Scanner (`v1.0.0`)

## 1. Actual Deployment Topology
Phishing URL Scanner is packaged as a self-hosted, single-process Python ASGI web application (`src/api/main.py`) backed by Uvicorn (`uvicorn==0.54.0`). No external cloud hosting provider, container registry, or database server is provisioned for `v1.0.0`.

- **Local Operator / Workstation Deployment:** Cloned from `https://github.com/calebfuller1705/capstone.git` at tag `v1.0.0`, bound to `http://127.0.0.1:8000` with `--workers 1`.
- **Automated CI Verification Environment:** `.github/workflows/ci.yml` executes `./script/setup`, `./script/lint`, `./script/test`, `./script/build`, starts the server in the background on `PORT=8000`, and verifies `POST /scan` via `./script/smoke`.

## 2. Deploying from an Annotated Release Tag (`v1.0.0`)
```bash
git clone [https://github.com/calebfuller1705/capstone.git](https://github.com/calebfuller1705/capstone.git)
cd capstone
git checkout v1.0.0
./script/setup
# Edit .env and set VIRUSTOTAL_API_KEY=<your-64-char-hex-key>
./script/start

On Windows PowerShell:
git clone [https://github.com/calebfuller1705/capstone.git](https://github.com/calebfuller1705/capstone.git)
Set-Location capstone
git checkout v1.0.0
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
Copy-Item .env.example .env
# Edit .env and set VIRUSTOTAL_API_KEY=<your-64-char-hex-key>
.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

## 3. Post-Deploy Verification & Rollback
Health check: GET http://127.0.0.1:8000/health returns {"status":"ok"} (HTTP 200).

End-to-end scan check: POST http://127.0.0.1:8000/scan with {"url":"https://example.com"} returns HTTP 200 with a JSON verdict object.

Rollback: Follow docs/runbook.md §2.4 (git checkout --force v0.9.0-rc.2 and restart Uvicorn; verified recovery time 6.43s in docs/rollback-transcript.txt).