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