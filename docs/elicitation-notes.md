# Elicitation Interview Notes

**Interviewee:** Corporate Employee / Non-Technical User
**Date:** 2026-08-29
**Role:** End User
**Duration:** 30 minutes

## Transcript & F/W/O Analysis
*(F = Fact about today, W = Want/Desire, O = Opinion)*

**1. "Walk me through the last time you did this. Start from the beginning."**
* **Interviewee:** "The last time I got a suspicious link, I first looked at the email to determine whether I recognized the sender. [F] I then looked at the URL itself and tried to determine whether the domain appeared legitimate. [F] If I still wasn't sure, I would avoid clicking it and try to find another way to determine whether it was legitimate. [F] The biggest problem was that I didn't have a simple way to determine whether the URL was actually safe. [O] I would have to rely on my own judgment or potentially ask someone in IT. [F]"
* **My Capstone Mapping:** Replace this manual process with a simple workflow: Receive link -> Copy -> Paste -> Submit -> Wait -> Receive clear Safe/Unsafe/Ambiguous result. The user shouldn't have to understand technical security information. [W]

**2. "What did you use to do it?"**
* **Interviewee:** "There isn't really a dedicated tool that I use currently. [F] I would usually inspect the URL myself, use a search engine, or ask someone with more technical knowledge. [F]"
* **My Capstone Mapping:** Use VirusTotal's API as the primary source. The application evaluates returned information and translates it. The user shouldn't see raw API responses. [W] 

**3. "Where did that go wrong the last time?"**
* **Interviewee:** "The biggest problem is uncertainty. [O] I can look at a URL, but I may not know whether a domain is legitimate or whether it has been associated with malicious activity. [F]"
* **My Capstone Mapping:** The information isn't always conclusive (mixed vendor flags). The app needs to account for invalid URLs, empty submissions, API errors/timeouts, rate limits, unscannable URLs, and ambiguous results. [F]

**4. "What did you do when it went wrong?"**
* **Interviewee:** "If I couldn't determine whether the link was legitimate, I would simply avoid clicking it and potentially ask IT for help. [F]"
* **My Capstone Mapping:** The system must provide a clear alternative to uncertainty. Instead of giving raw data, it must say safe, unsafe, ambiguous, or error. [W] The primary persona will abandon the tool and escalate to IT if results are confusing or slow. [F]

**5. "How often does this happen? How long does it take?"**
* **Interviewee:** "I encounter several suspicious links per week, although the exact frequency would depend heavily on the organization and individual. [F] It takes approximately 5–10 minutes per suspicious link because I may inspect the email and contact IT. [F]"
* **My Capstone Mapping:** Target timeframe is 10–30 seconds of user interaction. [W] The VirusTotal request must time out after 10 seconds. [F]

**6. "Who else touches this?"**
* **Interviewee/Analysis:** 
  1. The corporate employee receiving the link. [F]
  2. IT/helpdesk or cybersecurity personnel (affected when users escalate). [F]
  3. The technical maintainer (needs to know API keys, environment variables). [F]

**7. "If this problem disappeared tomorrow, what would change about your day?"**
* **Interviewee:** "I wouldn't have to spend as much time trying to determine whether suspicious links are legitimate. [F] Instead of researching the URL myself or immediately contacting IT, I could quickly submit the URL and receive a response. [W]"
* **My Capstone Mapping:** For the employee, the change is confidence and speed. For IT, it reduces basic Teams messages. [O]

**8. "What is the part I have not asked about?"**
* **Interviewee/Analysis:** What happens when the system can't confidently determine if something is safe? [F] I don't want a false sense of security; there must be clear distinctions (Safe, Unsafe, Ambiguous, Unable to analyze, Error). [W] Privacy and security are also concerns (what data is sent, how is the API key protected). [F] Handling of URL shorteners. [F]

---

## Post-Interview Analysis

### 1. Data Model (Nouns used >2 times)
* URL / Link
* IT / Helpdesk
* Information / Data
* API
* Domain
* Application / System
* User / Employee

### 2. Wrong Assumptions Corrected
1. **Assumption:** Users have a baseline tool they check before asking IT. 
   **Correction:** They don't have a dedicated tool; they use search engines or just guess.
2. **Assumption:** Users want to see the reasons why a link is bad. 
   **Correction:** Users actively *do not* want technical information; they just want a definitive Safe/Unsafe verdict.
3. **Assumption:** The main failure point is a "bad scan." 
   **Correction:** The main failure point is *uncertainty* (ambiguous results or slow loading) which immediately causes the user to abandon the app and message IT anyway.

### 3. Open Questions Identified
* How exactly are URL shorteners handled (scan the short link vs. follow the redirect first)?