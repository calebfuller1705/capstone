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

## 3. Options Considered & Pruned (Rep 3)

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