```mermaid
graph TD
    Client["🖥️ Web Client"]

    subgraph APIService ["⚙️ API Service Container (FastAPI)"]
        Router["🔌 api_router<br/>Job: Receives POST, handles HTTP responses"]
        Poller["⏱️ poller<br/>Job: Manages the 10s timeout and async retry loop"]
        VTClient["🛡️ vt_client<br/>Job: Holds API key, executes HTTP calls to VT"]
        Evaluator["🧮 evaluator<br/>Job: Parses VT stats into Safe/Unsafe verdict"]
    end

    VT["🌐 VirusTotal API"]

    Client -- "POST /scan {url}" --> Router
    Router -- "Passes URL" --> Poller
    Poller -- "Requests ID, then polls status" --> VTClient
    VTClient -- "HTTP POST/GET with API Key" --> VT
    VTClient -- "Returns raw JSON" --> Poller
    Poller -- "Passes raw JSON" --> Evaluator
    Evaluator -- "Returns {verdict: Safe/Unsafe}" --> Router