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

The system emits **one of four outputs**: flaky, genuine, infrastructure, or **abstain**.

**Why four, not three:**
- Abstain is the safety valve: when confidence is too low across all three causes, the system defers to engineer judgment (cost 700) rather than risk guessing wrong on "genuine" (cost 5000)

**Why this is not the same as the decision:**
- The engineer uses the system output + their judgment to decide action
- Engineer controls the release decision; system provides triage
- The engineer owns the call; the system provides evidence (or abstains)

## The Cost Matrix

| True Cause | System Output | Cost | Reason |
|-----------|---------------|------|--------|
| Flaky | Flaky | 0 | Correct |
| Genuine | Genuine | 0 | Correct |
| Infrastructure | Infrastructure | 0 | Correct |
| — | Abstain | 700 | Engineer manual logs investigation |
| Flaky | Genuine | 600 | Time waste, unnecessary escalation |
| Flaky | Infrastructure | 400 | Time waste, wrong investigation |
| Genuine | Flaky | **5000** | Broken code ships to production |
| Genuine | Infrastructure | 400 | Time waste, wrong investigation |
| Infrastructure | Flaky | 400 | Time waste, test rerun yields same result |
| Infrastructure | Genuine | 600 | Time waste, escalate engineer |

**The dominant risk:** Predicting flaky when actually genuine costs 5000. Shipping broken code is unacceptable.

**Key property:** Asymmetric cost. The system minimizes expected cost, not accuracy. Accuracy would treat all errors equally, which is false here.
