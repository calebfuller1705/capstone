# Walking Skeleton Traceability & Verification

**Project:** Stateless URL Security Scanner  
**Baseline Reference:** `spec-baseline-v1.0`  
**Execution Date:** 2026-10-15  

---

## 1. Request Path

| # | Hop | Component in My System | Real? | Evidence |
|---|---|---|:---:|---|
| 1 | Client / entry point | `ui_controller` (Vanilla HTML/JS single-input form) | No | `src/web/index.html` does not yet exist; only wireframed in architecture. |
| 2 | Route / dispatch | `api_router` (FastAPI `POST /scan` route handler) | Yes | `src/api/main.py` route is uncommitted; HTTP requests have no listening socket. |
| 3 | Service / domain | `poller` & `evaluator` (Async 10s loop & threshold scoring) | No | Logic exists only as specification text in `docs/architecture.md` § 4 & § 7. |
| 4 | External store / API | `vt_client` (VirusTotal v3 REST API client) | No | Python client wrapper unwritten; only verified via exploratory curl in `SP-01`. |
| 5 | Response | `api_router` (RFC 7807 JSON Problem / 200 OK envelope) | No | No serialization schema or HTTP response pipeline active. |
| 6 | Rendered result | `ui_controller` (DOM verdict banner & retry action button) | No | No DOM update script exists to translate JSON payload into visual state. |