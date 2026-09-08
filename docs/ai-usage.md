# ai-usage


## Spine Rule
I take full responsibility for every line of code, documentation, and configuration in this repository. If an AI writes it, I must understand it entirely before committing it. 

## The Zones
- **Green Zone (No log required):** Syntax lookups, fixing compiler errors, explaining error messages, and basic terminal commands.
- **Amber Zone (Must be logged):** Generating boilerplate code, drafting configuration files (like `.gitignore`), and brainstorming risk tables or project schedules.
- **Red Zone (Banned):** Generating the core logic of my application, writing the personal reflections in my charter (non-goals, definitions of finished), or asking the AI to make architectural decisions without my input.

## Tools I have decided to use
| Tool | Version | What I use it for | What I will NEVER use it for |
| :--- | :--- | :--- | :--- |
| Gemini | Current | Generating config boilerplates, syntax help, drafting Markdown structures | Writing my project purpose, non-goals, or final capstone code logic |
| GitHub Copilot | VS Code Extension | Inline code completion, auto-formatting boilerplate code, generating syntax for unit tests | Writing core algorithmic logic or making architectural decisions for the application |

## Log Entries

| Date | Tool | Prompt / Task | What it produced | What I changed | Why I changed it |
| :--- | :--- | :--- | :--- | :--- | :--- |

| 2026-08-25 | Gemini | "Generate a .gitignore for a Windows, VS Code, and Python stack" | A standard .gitignore file with OS, IDE, and Python exclusions | I manually reviewed the file and added `*.sqlite3` at the bottom | Added the database extension just in case I use a local SQLite store before moving to SQL Server |

| 2026-08-26 | Gemini | "Turn my 16-week Hat Map into a 15-hour/week calendar with blocked sessions" | A perfectly distributed 15-week daily schedule | I manually ripped out the generated hours for Weeks 8 and 14 and moved them to earlier weeks | The AI had no knowledge of my midterm exams or the Thanksgiving holiday break |

| 2026-08-30 | Gemini | "It is Week 16. This project failed and I am writing the post-mortem. Give me the three most likely causes... | Gave me the three most likely points of failure with a paragraph for each |

| 2026-09-02 | Gemini | "INTERROGATE prompt from section 3.8: twenty questions..." | 20 edge-case and failure-state questions | Answered 15 in my notes, moved the 5 I couldn't answer into Section 8 of my requirements doc | The model was extremely effective at finding failure states (like URL shorteners and exact scoring thresholds) that I hadn't formally defined yet |

| 2026-09-03 | Gemini | "FIND THE HOLES prompt from section 3.8" | 4 potential edge cases missing from requirements | Kept 1 (handling empty/corrupted JSON payloads). Discarded 3: extreme URL length is unlikely, API key expiration is already planned for, and double-clicking will be prevented by the UI hiding the submit button. | The AI found 1 genuine hole and 3 invented/already covered ones. Ratio of genuine to invented was 1:3. |

| 2026-09-07 | Gemini | Reformat these raw elicitation interview notes into the required rubric structure, including F/W/O tags and data model noun extraction. | A  structured Markdown document containing the transcript analysis and post-interview breakdown. | Kept all of it. The formatting accurately applied the F/W/O tags to my existing answers and correctly identified the nouns for the data model without altering the meaning of my raw notes. | Saved time on manual document structuring while ensuring all rubric requirements for the interview deliverable were met. |