# Problem Statement: CI Triage at 02:47

## The Decision

**Who:** On-call engineer (deployment owner)  
**When:** 02:47 AM (6 hours 13 minutes before 09:00 release deadline)  
**What:** How to categorize the failure and what action to take  
**By When:** Immediately (minutes, not hours)

The engineer sees a test failure. They need to know: Is this flaky? Real bug? Infrastructure hiccup?

## The Actions

After reading logs and understanding the failure, the engineer can:

1. **Rerun the test** — if likely flaky or infra issue
2. **Contact the code owner** — if likely a real issue caused by recent code
3. **Check infrastructure** — if likely an environment/transient issue
4. **Stop the release** — protective action taken first, pending triage

## The Prediction

The system estimates **probability for each root cause** (flaky, genuine, infra), rather than making the decision itself.

**Why this is not the same as the decision:**
- The engineer uses these probabilities + their judgment to decide action
- A 70% flaky estimate might still mean "rerun once, then escalate"
- The engineer owns the call; the system provides evidence

## The Cost

| Error Type | Cost | Why |
|-----------|------|-----|
| Predict genuine, actually flaky | 600 | Time waste, unnecessary escalation |
| Predict genuine, actually infra | 400 | Time waste, rerun yields same result |
| Predict flaky, actually genuine | **5000** | Broken code ships to production release |
| Predict infra, actually genuine | 400 | Time waste, rerun yields same result |
| Predict infra, actually flaky | 400 | Uncertain output, wastes time |
| Escalate to human | 500 | Always a cost (time, attention) |
| Correct prediction | 0 | System worked as intended |

**The dominant risk:** Calling it flaky when it's really a bug costs 5000. Shipping broken code is unacceptable.
