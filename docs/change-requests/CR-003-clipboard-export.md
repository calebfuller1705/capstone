# CR-001 — Quick-copy scan summary to clipboard

| Field | Value |
|---|---|
| Raised by | user, Week 12 usability testing |
| Date raised | 2026-11-06 |
| Baseline affected | spec-baseline-v1.0 |
| Request | "It would be great to have a single button that copies the URL verdict and stats to paste into Jira tickets." |

## Impact analysis

- **Cost:** 0.5 build + 0.5 test + 0.5 doc = 1.5 h; 26.5 h remain before the Week-14 freeze
- **Blast radius:** minor UI enhancement; `src/static/index.html`, `src/static/app.js`, and `src/static/styles.css`; touches browser DOM and Clipboard API; adds 1 integration test in `tests/integration/test_frontend_seam.py`; updates `docs/architecture.md`
- **Risk:** accept -> 1.5 of 28.0 remaining hours goes to a low-risk client feature with zero backend touchpoints; refuse -> users must manually highlight and copy multiple DOM text nodes to share triage results

## Decision

| Field | Value |
|---|---|
| Disposition | ACCEPT |
| Decided by | Caleb Fuller, 2026-11-06 |
| Rationale | High usability value with trivial blast radius; purely client-side and preserves the stateless zero-persistence architecture. |

## Applied

- [x] Requirements specification updated with minor usability requirement
- [x] Client DOM handler and copy button wired in `src/static/app.js`
- [x] Row added to the change table at the top of CHANGELOG.md
- [x] Traces: verified in browser seam tests, noted in Week-12 reps log