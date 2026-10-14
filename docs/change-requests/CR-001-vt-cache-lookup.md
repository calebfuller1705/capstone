# CR-001 — VirusTotal Cache Pre-Check Before Analysis Submission

| Field | Value |
|---|---|
| Raised by | Caleb Fuller |
| Date raised | 2026-10-14 |
| Baseline affected | spec-baseline-v1.0 |
| Trigger | Design Review peer finding DR-010: submitting all URLs to POST /api/v3/urls burns rate limit quota unnecessarily. |

## What Changes
In `docs/architecture.md` Section 5.1 and Section 7.1:
* **Before:** Backend always runs `POST /api/v3/urls` to get an `analysis_id`, followed by polling `GET /api/v3/analyses/{id}` for 10.0 seconds.
* **After:** Backend first does `GET /api/v3/urls/{base64_id}`. If VirusTotal gives HTTP 200 with `last_analysis_stats` generated within the last 24 hours, the backend evaluates the verdict immediately without putting in a new analysis or polling. If VT returns HTTP 404, the backend falls back to the existing `POST /api/v3/urls` polling flow.

## Why
The free-tier VirusTotal API allows only 4 requests per minute (`FR-API-01`, `R-02`). Repeatedly scanning common domains (e.g., `google.com`) burns two API calls per scan (submission + poll). Pre-checking the cache works safe/known URLs in a single HTTP call, cutting API consumption by 50% for repeat queries.

## Impact Assessment

| Dimension | Assessment |
|---|---|
| Requirements affected | `FR-SYS-01`, `FR-API-02` |
| Specification sections affected | `docs/architecture.md` § 5.1, § 7.1 (Flow 1) |
| Hours: added / removed | +2.0 hours (calibrated) |
| Schedule effect | Scheduled into Week 10 (WP-2 Backend Integration); absorbed by 14.25h project buffer without moving delivery gates. |
| Risk effect | Reduces exposure for `R-02` (VirusTotal Rate-Limiting Bottleneck) from $E=16$ down to $E=8$. |
| Definition of done effect | Requires one unit test asserting cache-hit bypass and one mocking a 404 fallback. |

## Decision

| Field | Value |
|---|---|
| Decision | Approved (Deferred to Week 10) |
| Decided by | Caleb Fuller |
| Date | 2026-10-14 |
| Rationale | Approved because it preserves critical API quota during user testing while protecting the Week 9 Walking Skeleton milestone from branching logic. |

## Applied

- [x] Specification updated and committed
- [x] Traceability matrix updated
- [x] Plan and hours re-baselined
- [x] Row added to `CHANGELOG.md`
- [ ] Implementation scheduled for Week 10 (WP-2)