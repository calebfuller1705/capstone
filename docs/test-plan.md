# Test Plan — URL Security Scanner

**Version:** 1.0  ·  **Author:** Caleb Fuller  ·  **Date:** 2026-10-29  ·  **Baseline commit:** <sha>

---

## 1. Scope — what is under test

This plan covers verification and validation for functional requirements FR-1 through FR-6 and non-functional requirements NFR-1 and NFR-2 at the baseline commit. Verification makes sure that target URLs are validated and normalized (FR-1), queried against VirusTotal v3 through base64url encoding (FR-2), queued for asynchronous processing on missing reports (FR-3), combined across engine detections (FR-4), measured for scan latency (FR-5), put into standardized HTTP status codes on errors (FR-6), kept by a 5.0-second fail-fast timeout (NFR-1), and run under strict zero disk persistence and in-memory credential boundaries (NFR-2).

## 2. Out of scope — what is NOT under test, and why

- **Persistent database storage and disk query caching:** NFR-2 says zero disk persistence and in-memory execution boundaries; no disk database or persistent cache will be implemented or tested.
- **File and binary payload scanning:** The system boundary is bounded to URL inspection and VirusTotal v3 URL threat analysis; binary artifact upload and sandbox emulation are excluded.
- **Live third-party API consumption in automated CI:** Third-party public quotas enforce a 4 req/min rate limit that induces non-deterministic test flakiness and quota exhaustion; CI runs against stubs, fixtures, and local mock adapters.

## 3. Test levels

| Level | What it covers here | How it runs | Roughly how many |
|---|---|---|---|
| Unit | URL normalization, unpadded base64url encoding, schema validation, latency calculation | `pytest tests/unit/` | 15–25 |
| Integration | VirusTotal v3 client seams, 404 cache misses, 429 rate limit responses, 5.0s socket timeouts | `pytest tests/integration/` | 5–10 |
| Acceptance | End-to-end FastAPI endpoint contracts (`POST /scan`, `GET /health`), zero-persistence assertions | `pytest tests/acceptance/` | 6–8 |

## 4. Environment

| Item | Value |
|---|---|
| Runtime / language version | Python 3.11+ |
| Operating system(s) | Windows 11 / Linux (ubuntu-latest GitHub Actions runner) |
| Database / storage | None (stateless in-memory execution per NFR-2)[cite: 1] |
| Third-party services | VirusTotal v3 API (stubbed via `unittest.mock` / `respx` in CI)[cite: 2] |
| Test data set | `docs/demo-seed.json` (committed deterministic test cases) |
| Where it runs | Local PowerShell and GitHub Actions CI (`.github/workflows/ci.yml`) |

## 5. Entry criteria — we may begin testing when

- [x] The build under test is tagged and pushed; CI is green on the pipeline from Chapter 9.
- [x] Every Must requirement has at least one written test case.
- [x] The test data set is checked in and loads without manual steps.
- [x] Local virtual environment dependencies are locked and passing static analysis (`flake8`).

## 6. Exit criteria — verification is DONE when

- [ ] 100% of Must requirements (FR-1, FR-2, FR-6, NFR-1, NFR-2) have at least one passing acceptance test in `docs/traceability.csv`[cite: 1, 2].
- [ ] 0 open defects at severity S1 or S2[cite: 2].
- [ ] Every open S3/S4 defect appears in `docs/defect-log.md` with a documented workaround[cite: 2].
- [ ] Every defect fixed this iteration has a named regression test that fails on the old code[cite: 2].
- [ ] The full suite runs from one documented command (`pytest` / `script/test`) and passes in CI[cite: 2].
- [ ] Response latency for upstream socket hangs aborts in <= 5.0 seconds, and mocked endpoint response time is <= 500 ms p95 (NFR-1)[cite: 1, 2].

## 7. Risks to the testing itself

| Risk | Trigger | Response |
|---|---|---|
| Upstream schema drift in VirusTotal v3 | Upstream response changes field types or missing keys | Defensive dictionary access (`.get()`) and typed Pydantic models with validation tests |
| Upstream rate limiting in test runs | HTTP 429 status code encountered | Mock network I/O in CI by default and flag live API calls[cite: 2] |

## 8. Schedule

| When | What |
|---|---|
| Week 11, days 1–2 | Test plan, test case derivation, traceability matrix |
| Week 11, days 3–5 | Write and automate the suite; first full pass |
| Week 11, days 6–7 | Triage, fix S1/S2, regression tests, log |

## 9. Approval

I have read this plan and I am accountable for the exit criteria above.

Signed: Caleb Fuller  ·  Date: 2026-10-29