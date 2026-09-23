```mermaid
graph TD
    User["👤 Corporate Employee"]
    VT["🌐 VirusTotal v3 API<br/>(3rd Party, 500 req/day)"]
    Ping["⏲️ Uptime Monitor"]

    subgraph Untrusted [Client-Side / Untrusted]
        Client["🖥️ Web Client<br/>Tech: Vanilla HTML/JS<br/>Resp: Input validation, a11y UI rendering"]
    end

    subgraph Trusted [Server-Side / Trust Boundary]
        API["⚙️ API Service<br/>Tech: Python / FastAPI (Render)<br/>Resp: Holds API Key, polls VT, enforces 10s timeout"]
    end

    User -- "Types URL, clicks submit" --> Client
    Client -- "POST {url: string}<br/>Protocol: HTTPS/JSON" --> API
    API -- "POST url, GET analysis<br/>Protocol: HTTPS/JSON (w/ secret header)" --> VT
    Ping -- "GET /health<br/>Protocol: HTTPS" --> API