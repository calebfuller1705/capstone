# Iteration 1 Plan: Core Slices (Week 10)

## Slice 1: Upstream VirusTotal v3 API Client Integration (FR-2)

* **SLICE:** FR-2 The scanner retrieves live threat intelligence reports for submitted URLs from the VirusTotal v3 API.
* **Layers:** Client (`POST /scan`) → Route Handler (`src/api/main.py`) → Domain Service (`src/services/vt_client.py`) → Upstream Integration (`VirusTotal GET /api/v3/urls/{id}`).
* **Demo in one sentence:** Submit a known public URL (e.g., `https://google.com`) and display live stats returned directly from VirusTotal rather than a hardcoded stub.
* **Acceptance criteria to satisfy:**
  - [ ] Generates unpadded base64url SHA-256 identifier per VirusTotal v3 specification.
  - [ ] Sends `x-apikey` header read just from `VIRUSTOTAL_API_KEY` environment variable.
  - [ ] Returns HTTP 200 with raw analysis statistics when the URL exists in cache.
* **Estimate (three-point):** Optimistic 2.0 h | Likely 3.5 h | Pessimistic 5.0 h
* **Riskiest unknown:** Upstream network timeouts, base64 URL identifier formatting nuances, and response schema discrepancies across different URL submission states.


## Slice 2: Threat Engine Verdict Aggregation (FR-4)

* **SLICE:** FR-4 The scanner evaluates individual engine detections and loads an actionable security verdict (`Safe`, `Suspicious`, or `Malicious`).
* **Layers:** Route Handler (`POST /scan`) → Aggregation Engine (`src/domain/verdict.py`) → Serialization Model (`ScanResponse`) → Client JSON Output.
* **Demo in one sentence:** Submit a clean URL to see a `Safe` verdict, and submit a known test malicious URL (e.g., EICAR) to see a flagged `Malicious` verdict with detection counts.
* **Acceptance criteria to satisfy:**
  - [ ] Categorizes verdicts strictly: $\ge 3$ malicious detections $\rightarrow$ `Malicious`; $1\text{--}2$ $\rightarrow$ `Suspicious`; $0$ $\rightarrow$ `Safe`.
  - [ ] Serializes response to enforce the baselined contract (`url`, `verdict`, `source`, `scan_time_ms`).
  - [ ] Unit tests verify threshold edge boundaries without doing live network calls.
* **Estimate (three-point):** Optimistic 1.5 h | Likely 2.5 h | Pessimistic 3.5 h
* **Riskiest unknown:** Handling divergence between "suspicious" vs. "malicious" across legacy threat engines while avoiding false positives.


## Slice 3: URL Ingress Normalization & Input Validation (FR-1)

* **SLICE:** FR-1 The scanner validates incoming URL strings, rejecting invalid formats and unroutable addresses before executing scans.
* **Layers:** Client (`POST /scan`) → Pydantic Validator (`src/api/schemas.py`) → Normalizer (`src/domain/normalize.py`) → Route Ingress.
* **Demo in one sentence:** Attempt to scan malformed URLs, missing schemes, or private IPs and receive HTTP 422 validation errors immediately.
* **Acceptance criteria to satisfy:**
  - [ ] Normalizes valid URLs (adds missing trailing slash to root domains, converts schemes to lowercase).
  - [ ] Rejects inputs without `http`/`https` schemes, private IP ranges (`10.0.0.0/8`, `192.168.0.0/16`, `127.0.0.1`), and malformed strings with HTTP 422.
  - [ ] Unit tests assert edge cases including punycode, long query parameters, and embedded credentials.
* **Estimate (three-point):** Optimistic 1.0 h | Likely 2.0 h | Pessimistic 3.0 h
* **Riskiest unknown:** Edge cases in RFC 3986 parsing where malformed URLs go past standard regex or string splitting and crash downstream HTTP handlers.


## Slice 4: Upstream Error & Rate Limit Handling (FR-6)

* **SLICE:** FR-6 The scanner handles upstream API outages, rate limits (HTTP 429), and network failures without crashing or leaking credentials.
* **Layers:** Upstream Client (`src/services/vt_client.py`) → Exception Middleware (`src/api/errors.py`) → Standardized Error Response.
* **Demo in one sentence:** Simulate an upstream 429 or missing API key and show a clean HTTP 429/503 response containing retry guidance and zero internal traces.
* **Acceptance criteria to satisfy:**
  - [ ] Translates upstream 429 to client HTTP 429 with `Retry-After` header.
  - [ ] Maps upstream network timeouts and 5xx errors to client HTTP 503 Service Unavailable.
  - [ ] Enforces that API keys and environment variables never appear in logs or client-facing responses.
* **Estimate (three-point):** Optimistic 1.0 h | Likely 2.0 h | Pessimistic 3.5 h
* **Riskiest unknown:** Consistent behavior of async HTTP client timeouts (`httpx.TimeoutException` vs. raw socket disconnects) across differing host environments.


## Rep 2: Board Task Audit (Vertical vs. Horizontal)

| Issue # | Title | Type | Action / Resolution |
| :--- | :--- | :---: | :--- |
| #1 | [FR-1] Validate and normalize target URL inputs | V | Standalone slice (ingress validation) |
| #2 | [FR-2] Integrate VirusTotal v3 API client for URL report lookup | V | Standalone slice (upstream integration) |
| #3 | [FR-3] Handle asynchronous scan submissions when URL report is missing | V | Standalone slice (polling loop) |
| #4 | [FR-4] Combine multi-engine detection statistics into unified verdict | V | Standalone slice (domain scoring) |
| #5 | [FR-5] Compute and serialize scan execution latency | H | Folded into [FR-4] response contract |
| #6 | [FR-6] Map upstream API error states and 429 rate limits | V | Standalone slice (handled failure paths) |
| #7 | [NFR-1] Enforce 5-second fail-fast timeout on upstream calls | H | Folded into [FR-2] client configuration |
| #8 | [NFR-2] Guarantee zero disk persistence and in-memory boundaries | H | Kept standalone as architectural audit gate |