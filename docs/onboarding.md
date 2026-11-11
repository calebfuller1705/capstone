## Onboarding Guide

# Feature-to-Code Map
| Feature a user would name | Where it lives | Its test| 
| URL Input Validation & Bounds Checking | src/api/schemas.py | tests/unit/test_url_validation.py |
| VirusTotal v3 Upstream Client & Polling | src/services/vt_client.py | tests/unit/test_vt_client.pytests/integration/test_vt_contracts.py | 
| SSRF Guard & Hostile Boundary Enforcement | src/api/main.py src/api/schemas.py | tests/security/test_security_review.pytests/unit test_hostile_data.py | 
| Web UI Interaction & Verdict State Rendering | src/static/app.js src/static/index.html | tests/integration/test_frontend.py | 
| System Health & Uptime Ping Endpoint | src/api/main.py | tests/unit/test_health.py

## Good First Issue: B-04 (Slice 1) — File-Based Error Code Audit Logger (FR-SYS-02)

# Context & Objective:

During the Week 12 scope cut, server-side action logging (FR-SYS-02 / Backlog item B-04) was deferred because full transaction logging conflicted with privacy constraint CON-04 (zero-persistence) and required dedicated disk volume orchestration. This introductory task implements an isolated, privacy-safe slice: logging only unhandled upstream API error codes to a local text log, without logging sensitive user URLs or query strings.

# File to Open:
src/api/main.py

# What to Do:
Add a helper function log_system_error(error_code: str) -> None that appends a single line formatted as ISO8601_UTC [ERROR] <error_code>\n to a local file at logs/audit_errors.log.

Ensure the function creates the logs/ directory if it does not already exist, and wraps file I/O in a safe try...except OSError block so logging failures never interrupt request dispatch.

Wire this helper into the exception handler for upstream 502/504 errors in src/api/main.py.

# Test to Run:
Execute integration fault tests to verify the exception handler continues to return the RFC 7807 problem detail envelope:

Bash
pytest tests/integration/test_dependency_faults.py -v

# What "Done" Looks Like:
When an upstream mock raises a timeout or 502 error during tests, logs/audit_errors.log contains an entry such as 2026-11-11T19:30:00Z [ERROR] UPSTREAM_TIMEOUT.

Zero URL strings, IP addresses, or payload bodies are written to the file (preserving NFR-SEC-02).

All existing tests in tests/integration/test_dependency_faults.py remain green.

# Estimated Time:
1 to 2 hours.
