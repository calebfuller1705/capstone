# Feature areas and the identifier scheme

AREA CODE,AREA NAME,ONE SENTENCE OF SCOPE
INP,Input,Everything about the user submitting and validating a URL.
API,External APIs,Everything about securely querying VirusTotal and handling network responses.
EVAL,Risk Scoring,Everything about translating raw JSON thresholds into a boolean safe/unsafe verdict.
DASH,Dashboard,Everything about loading the final risk score in plain English for a non-technical user.

# The persona set, with evidence

| Persona | Who | Needs | Constraining behavior | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Corporate Employee** (Primary) | A non-technical office worker who frequently receives external emails. | To instantly know if a link is safe to click without parsing technical data. | Will close the app and escalate to the IT helpdesk if the results are confusing or take too long to load. | Interview 2026-08-29; quoted stating they "have no clue whether it is real." |
| **The next maintainer** | The person who clones the repository in Week 17 knowing nothing about it. | To understand what every feature was for, from the document alone. | Will fail the deployment test if environment variables and API keys are not clearly documented in a setup file. | The course's own handoff test. |