# The Week-12 Security Pass — checklist and evidence sheet

Two rules before you start:

- **Evidence beats assertion.** "Inputs are validated" is a claim. "Every write endpoint rejects
  the payloads in `tests/security/test_input.py`; run `pytest tests/security`" is evidence.
- **A finding you cannot fix this week is not a failure — an undocumented one is.** Record it as a
  defect with a severity and a disposition, exactly as in Week 11.

For the current category list and cheat sheets, use the OWASP project pages
(<https://owasp.org/www-project-top-ten/>). The category names and numbering are revised
periodically, so read the current edition rather than a remembered list.

---

## The seven areas

| # | Area | The question to answer | Evidence | Finding | Disposition |
|---|---|---|---|---|---|
| 1 | **Secrets** | Is any credential in the repository, in its history, in a log, or in a screenshot? | Ran `git grep -nIE '(AKIA[0-9A-Z]{16}\|BEGIN [A-Z ]*PRIVATE KEY)'` (0 matches). Ran `git ls-files --error-unmatch .env` (clean, un-tracked). Automated test `pytest tests/security/test_security_review.py::test_security_secrets_not_leaked_in_scan_response` asserts API key is never serialized to JSON or response headers. | Zero credentials committed to tracked files or Git history. `.env` is ignored by `.gitignore`; `.env.example` committed. Key injected exclusively via OS environment variables. | Clean / Verified |
| 2 | **Input** | Does every externally supplied value get validated and safely parameterized before it reaches a query, a shell, a path, or a template? | Ran `pytest tests/security/test_security_review.py::test_security_input_ssrf_private_ip_rejection` and `::test_security_input_oversized_payload_rejected`; `pytest tests/unit/test_url_validation.py`. | Pydantic schema `ScanRequest` strips whitespace, enforces 2048-char ceiling, requires `http://` or `https://` schemes, and blocks private/loopback/cloud metadata IP ranges (`127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`, `169.254.169.254`) with HTTP 422 before any network I/O. Zero shell commands or SQL queries exist in codebase. | Clean / Verified |
| 3 | **Authentication** | Can a request act as a user without proving it is that user? Are sessions and password storage handled by a maintained library rather than by you? | Inspected `src/api/main.py` route definitions and architecture contract `CON-04` / `docs/architecture.md` §3. | The system is strictly stateless with zero user accounts, zero sessions, and zero database persistence (`CON-04`). There is no user identity to spoof. Outbound third-party authentication is handled exclusively by `src/services/vt_client.py` using the `x-apikey` HTTP header. | Clean (N/A by stateless design) |
| 4 | **Authorization** | For every object a user can name, is ownership checked *server-side* on every request — not just hidden in the UI? | Ran `pytest tests/security/test_security_review.py::test_security_authorization_no_object_by_id_endpoints`. | The server stores zero scan records, history logs, or user artifacts (`NFR-SEC-02`). There are zero endpoints exposing objects by ID (`GET /scan/{id}` and `/analyses/{id}` return HTTP 404/405). Cross-tenant object enumeration (IDOR) is architecturally impossible. | Clean / Verified |
| 5 | **Transport & storage** | Is traffic HTTPS end to end? Is anything sensitive stored that you do not actually need? | Verified `VT_BASE_URL = "https://www.virustotal.com/api/v3"` in `src/services/vt_client.py`. Ran `pytest tests/integration/test_tier1_seams.py::test_seam_partial_failure_zero_disk_persistence`. Production Render hosting terminates TLS 1.3. CORS locked via `CORSMiddleware` (DR-005). | External API traffic is encrypted via HTTPS. Zero bytes of scan history or URL data are persisted to disk or external storage (`NFR-SEC-02`). In-memory cache is ephemeral (TTL 300s) and contains no user PII. | Clean / Verified |
| 6 | **Dependencies** | Does any direct or transitive dependency carry a published advisory? Which, and what did you do? | Ran `pip-audit` against `.venv`. Verified report against GitHub Advisory Database and OSV.dev. | Detected `PYSEC-2026-4320` in `certifi==2026.7.22`[cite: 2]. Reachable via `httpx` TLS trust store during outbound VirusTotal queries. Upgraded to `certifi>=2026.10.18`[cite: 2]. Re-ran `pip-audit` to confirm zero vulnerabilities. | Fixed & Verified |
| 7 | **Errors & logging** | Do error responses leak stack traces, queries, paths, or tokens? Do logs contain secrets or personal data? | Ran `pytest tests/security/test_security_review.py::test_security_error_no_stack_traces_leaked` and `pytest tests/integration/test_tier1_seams.py::test_seam_error_semantics_timeout_mapping`. | DEF-003 previously allowed unhandled upstream socket timeouts to surface 500 error tracebacks. Resolved: `src/api/main.py` maps `UpstreamServiceError` to RFC 7807 problem details (HTTP 502/504) and catches unexpected exceptions with a sanitized HTTP 500 envelope. | Fixed (DEF-003) |

---

## Area 1 — Secrets: the commands

Search tracked files *and* history. Deleting a key in a later commit does not remove it.

```sh
# Tracked files, obvious literals. Widen the pattern for your provider's key format.
git grep -nIE '(AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|(api[_-]?key|secret|token|password)[[:space:]]*[:=][[:space:]]*[^[:space:]]{12,})'

# Every version of every file that ever existed.
git rev-list --all | xargs -n1 -I{} git grep -nIE 'AKIA[0-9A-Z]{16}' {} 2>/dev/null | head

# Is the environment file tracked by accident?
git ls-files --error-unmatch .env 2>/dev/null && echo "TRACKED - fix this"
```

## Area 6 — Dependencies: check the advisory, not the vibe

Run whatever your ecosystem provides — for example `npm audit`, `pip-audit`, `cargo audit`, or your
platform's dependency-scanning alerts — then verify each reported issue against a primary source:

- GitHub Advisory Database — <https://github.com/advisories>
- OSV — <https://osv.dev/>
- NVD — <https://nvd.nist.gov/>

Record each one:

```
| Advisory ID | Package | Version in use | Severity (CVSS v3.1) | Reachable from my code? | Action |
|---|---|---|---|---|---|
| PYSEC-2026-4320 | certifi | 2026.7.22 | 6.1 Medium | yes, root CA store used by httpx for VirusTotal HTTPS calls | upgraded to certifi>=2026.10.18; re-audit confirmed clean |
```

Under CVSS v3.1 the qualitative bands are None 0.0, Low 0.1–3.9, Medium 4.0–6.9, High 7.0–8.9,
Critical 9.0–10.0. "Reachable from my code?" is the column students skip and professionals live by:
a critical advisory in a code path you never call is a different decision than a medium one in your
login flow.

**If an assistant told you about a vulnerability, the advisory ID it gave you is the claim, not the
proof.** Paste the ID into the advisory database. Fabricated and mis-numbered identifiers are a
routine failure mode. No ID in the database, no line in this table.

---

## Sign-off

```
Security pass performed by: Caleb Fuller  Date: 2026-11-05
Areas covered: 1 2 3 4 5 6 7      Findings opened: 3   Fixed: 3   Accepted: 0
Highest-severity issue shipping in this release candidate: None (Zero open Critical or High defects; DEF-003, SSRF input validation, and certifi CVE fixed and verified)
```