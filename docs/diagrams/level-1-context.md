```mermaid
graph TD
    User["Corporate Employee<br/>(Submits links, views results)"]
    System["URL Security Scanner<br/>(Analyzes URLs for threats)"]
    VT["VirusTotal v3 API<br/>(3rd Party Threat DB)"]
    Ping["Uptime Monitor<br/>(Daily health check)"]

    User -- "Submits URL string" --> System
    System -- "Looks up risk score" --> VT
    Ping -- "Pings /health endpoint" --> System