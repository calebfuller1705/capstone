# Spike SP-01 — VirusTotal API Connection and Parsing

- **Unknown:** Can I successfully submit a URL to the VirusTotal v3 API, authenticate with my free-tier key, and parse out the specific 'malicious' and 'harmless' counts?
- **Feeds:** ADR 0002 — Third-party security API integration
- **Requirements at risk:** FR-SYS-01, NFR-SEC-01
- **Time box:** 90 minutes
- **Run on:** 2026-09-17

## The question
Can a standalone Python script submit a URL to the VirusTotal v3 API using a free-tier key and successfully bring back the exact integer counts for "malicious" and "harmless" votes in under 10 seconds?

## The smallest thing that answers it
A single Python script (`spike.py`) using the standard `requests` library.
* Hardcoded test URL.
* Hardcoded API key in the headers.
* Gives me the raw JSON response and the parsed integers to the terminal.
* No web framework (no FastAPI), no frontend, no error handling beyond printing the HTTP status code.

## Success criterion
The script prints a dictionary containing the exact integer counts for "malicious" and "harmless" for the submitted URL within 10 seconds of run time.

## Failure criterion
The free tier key is rejected for URL analysis, the JSON shape does not contain straightforward vote counts, or the API needs complex asynchronous polling that consistently takes longer than 10 seconds.

## Plan B if it fails
Fall back to the older VirusTotal v2 API if it is simpler/synchronous, or switch the integration to the Google Safe Browsing API (which means I need to update the functional requirements). 

## Result
*Timer stopped at: 77 minutes.*
The spike worked, but showed me a critical workflow detail. The VirusTotal v3 API needs a two-step process for *new* URLs: first you submit the URL to get an analysis ID, then you query that ID to get the numbers. However, if you query a URL that has already been scanned by someone else, you can get the stats in one step. The free tier key worked wonderfully, and the JSON response gave a `last_analysis_stats` object with exactly the integers I need. Latency for a known URL was ~800ms.

## Decision
Use the VirusTotal v3 API. The backend needs to be designed to deal with the two-step polling process gracefully for unknown URLs. This means the frontend loading indicator is very critical to keep the user waiting while the backend does the second API hop. ADR 0002 will show this dependency.