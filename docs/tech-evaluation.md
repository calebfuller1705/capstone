# Technology Evaluation


## 1. Architectural Drivers

| Driver | Requirement ID | Why it constrains the stack |
| :--- | :--- | :--- |
| **API Key Obfuscation** | FR-SYS-01 / NFR-SEC-01 | Rules out a pure frontend architecture; needs a secure backend server to have the VirusTotal API key and proxy requests. |
| **Strictly Stateless** | CON-04 | Rules out bulky web frameworks that need or assume constant database connections or session management. helps lighter frameworks. |
| **Zero Budget / Free Hosting** | CON-03 | Rules out paid managed services like AWS. The backend must be runnable on a free tier that allows the chosen language. |
| **57-Hour Solo Budget** | CON-01 / CON-02 | Rules out taking on a tech stack with a big novelty load. I need to use languages I am familiar with to make sure the budget is spent on product quality, not tutorials. |

**Summary:** The URL Security Scanner is a stateless, secure proxy for the VirusTotal API. It needs a lightweight backend to hide the API key and a simple frontend to show the results, all runnable to a free hosting tier. Because of the strict time budget, I will rely heavily on familiar programming languages for the backend web server to keep the novelty load at a level I can manage.


## 2. The Job-Board Test

| Technology | The real reason | Driver or résumé? |
| :--- | :--- | :--- |
| **Python / FastAPI** | I want to utilize my existing Python knowledge but learn a modern, highly employable framework that works with APIs well. | Résumé / Driver overlap |
| **React (Frontend)** | It seems to be the most requested frontend on most entry-level job postings. | Résumé |
| **Render (Hosting)** | Modern PaaS that employers use, and people say it has a solid free tier. | Driver (CON-03 requires zero budget) |

**Honest Motive Statement:** 
I want to use technologies that will make me employable. While I want to learn highly-demanded things like React, my primary driver is being able to produce a working product inside of my 57-hour budget constraint. If a heavily-requested résumé boosting technology costs me too much learning time, I will go to a simpler, boring technology to make sure the project actually finishes.

## 3. Options Considered & Pruned

I expanded the option space for three major decisions and pruned them to candidates I can have for a 57-hour solo project:

**Decision 1: Backend API (The Server)**
*   Kept: FastAPI (Python), Flask (Python)
*   Pruned: Express.js (Node), Spring Boot (Java), Django (Python). Reason: Too much novelty load or way too bulky for a simple stateless proxy.

**Decision 2: Frontend Tech (The UI)**
*   Kept: Vanilla HTML/JS, React
*   Pruned: Vue, Angular, Svelte. Reason: If I spend my novelty load token on my frontend, I will spend it on React for the most job-board relevance. The others kind of distract my focus.

**Decision 3: Hosting (The Infrastructure)**
*   Kept: Render, PythonAnywhere
*   Pruned: AWS EC2, DigitalOcean Droplet, Heroku. Reason: AWS/DO need manual Linux server administration, which would require much more time than I have, and Heroku does not have a free tier anymore.


## 4. Evaluation Rankings

*   **Backend:** FastAPI (4.20), Flask (4.15). *These are both in 0.25 of each other, making this a coin flip. The tiebreaker for me would be that Flask is much easier to reverse and has no novelty load, but I will intentionally choose to spend my one "Innovation Token" here to learn FastAPI for its job board relevance. (See ADR 0001).*
*   **Frontend:** Vanilla HTML/JS (4.40), React (2.40). *React loses big time. My 57-hour solo budget (CON-01/02) cannot take on the novelty load of learning a frontend build pipeline.*
*   **Hosting:** Render (4.40), PythonAnywhere (3.20). *Render wins because of its push-to-deploy capability.*


## 5. The Sensitivity Pass

I tested the fragility of the Frontend decision by taking half the weight of my highest criterion ("Low novelty load", from 0.50 down to 0.25) and putting the 0.25 difference to the other two criteria. 
*   **Did the winner change?** No. Even with novelty load going down, Vanilla JS still scored 4.025 against React's 3.15. The decision to use Vanilla JS i not dependent on a single guessed weight.


## 6. Seam Inventory

| Seam | What has to work | Crossed before? | Risk | Spike |
| :--- | :--- | :--- | :--- | :--- |
| **Backend ↔ VirusTotal API** | Python HTTP request, sending the API key securely, dealing with the 429 rate limit, parsing the JSON risk score. | No | High | SP-01 |
| **Backend ↔ Host (Render)** | Deploying a FastAPI `uvicorn` server to Render's free tier and securely putting in the API key as an environment variable. | No | Medium | SP-02 |
| **Frontend ↔ Backend** | Vanilla JS `fetch()` call sending the URL to the FastAPI endpoint and updating the DOM with the response. | Yes | Low | -- |

**Highest Risk Seam:** The Backend ↔ VirusTotal API seam scares me the most. If I cannot correctly format the request, authenticate with my free-tier key, or parse the specific malicious/harmless flags out of their JSON response, the entire function of the app fails.

## 7. Novelty Load

**Novelty Load Count: 2** (FastAPI and Render).
*   **Assessment:** A novelty load of 2 is manageable, but I can see how it would be dangerous because FastAPI and Render are on the exact same seam (Backend ↔ Host). If a deployment fails, I won't know right away if it's a FastAPI configuration issue or a Render environment issue.
*   **Action Plan:** Because they are on the same seam, I will need to spike both of them early (Weeks 5-7). I will budget learning hours in Week 7 for configuring Render deployments.
*   **Innovation Token:** I am spending my one "Innovation Token" on FastAPI. Even though Flask would be a novelty load of 0, learning FastAPI helps me in my employability goals and handles stateless API routing natively (CON-04).