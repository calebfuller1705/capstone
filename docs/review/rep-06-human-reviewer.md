# Rep 6: Human Peer Review Report

**Reviewer:** Luke Witte  
**Materials Reviewed:** Tag `spec-review-candidate` (`docs/requirements.md` § 5–6, `docs/architecture.md` § 4–6)  
**Time Box:** 45 minutes reading, 45 minutes walkthrough  
**Role Assumed:** Recorder

## 1. Walkthrough Notes & Probing Questions

When discussion got slower, I asked the two diagnostic questions mandated by Chapter 8:

1. **"What would you need to know that isn’t here?"**
   * *Reviewer response:* "I don't see how you stop someone from writing a Python script with `requests.post()` with your Render URL and going through your daily VirusTotal quota in twenty seconds. You don't have authentication, so without server-side request slowing down, your scanner can be DoS'd by one person."
   * *Result:* Logged as `DR-009` (Major).

2. **"Which part would you be most nervous to build?"**
   * *Reviewer response:* "The two-step VirusTotal flow. You assumed that submitting a URL always needs an analysis polling loop. In reality, VirusTotal v3 has it so that you get the existing cached URL analysis directly by hashing the URL into an ID. If you force a fresh analysis on every submission, you will hit rate limits much faster I think."
   * *Result:* Logged as `DR-010` (Major).