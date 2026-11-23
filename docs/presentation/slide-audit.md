### BEFORE (41 words, 6 adjectives, 0 verifiable decisions)
Technology & Hosting Choices
- I chose high-performance Python backend with FastAPI
- Uvicorn provides a lightweight, scalable ASGI web server
- An intuitive in-memory caching layer makes repeated lookups seamless
- Overall the deployment architecture is simple, fast, and follows best practices

## AFTER (Decision-Slide Pattern — ADR-0003 & NFR-PERF-01)
ADR-0003 — Single-Worker Uvicorn + 300s RAM Cache

Chose:      1 Uvicorn worker + 300-second in-memory TTL cache
Rejected:   Multi-worker cloud hosting without shared cache
Because:    VirusTotal free tier caps at 4 lookups/minute (`ADR-0004`)
Costs me:   Cache clears on restart; single-process concurrency ceiling
Evidence:   p95 dropped 83% to 184.22 ms (docs/performance.md, 2026-11-04)

The Six-Foot Test

### First-Pass Audit Notes (Per Slide Fixed)
- **Slides 1–20 (Global Typography Pass):** Enlarged secondary body text, bullet sub-labels, table cells, and source citations from sub-24 pt defaults up to a strict `24 pt` minimum (`30 pt` for primary claims and headers) so every element is legible from six feet back without squinting.
- **Slide 7 (Architecture Diagram) & Slide 8 (Data Model):** Increased box labels and arrow annotations to `24 pt` high-contrast black-on-white text so component boundaries (`Browser UI` -> `FastAPI SSRF Guard` -> `VirusTotal v3`) read cleanly at distance.
- **Slides 9–10 (Decision Slides) & Slides 14–16 (Evidence Tables):** Standardized `Chose / Rejected / Because / Costs me / Evidence` labels and metric table rows to `24 pt` bold/regular contrast.