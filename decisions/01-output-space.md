# Output Space: Why Four Outputs (Phase 01)

## Starting Point: Three Outputs

From phase 00, we have three root causes and three corresponding outputs:
1. Flaky — rerun the test
2. Genuine — contact the engineer
3. Infrastructure — check infrastructure

## The Case That Forces a Fourth

**Scenario:** Test failure at 02:47. Low confidence on all three causes:
- Probability flaky: 35%
- Probability genuine: 30%
- Probability infrastructure: 35%

The system must pick one. But:
- If we say "flaky" and it's actually "genuine" → ship broken code → cost 5000
- If we say "genuine" and it's actually "flaky" → waste time escalating → cost 600
- If we say "infrastructure" and it's actually "genuine" → waste time checking infra → cost 400

With uniform uncertainty, picking any of the three is risky. The cost of guessing wrong on "genuine" is catastrophic.

## The Fourth Output: Abstain

**What it means:** "I cannot distinguish with confidence. Engineer, read the logs yourself."

**What happens downstream:**
- Engineer manually investigates CI logs and test output
- Engineer uses judgment + context to pick flaky/genuine/infra
- System is not the bottleneck; it defers to human judgment

**Why abstain is wired to something:**
- Cost of abstain: ~700 (engineer's time for manual investigation)
- Cost of wrong guess on genuine: 5000
- Cost of wrong guess on other causes: 400-600

Abstaining is cheaper than confidently guessing wrong on the catastrophic case.

## Output Space: Final

| Output | Emitted When | Downstream Action |
|--------|--------------|-------------------|
| Flaky | High confidence flaky, low risk of genuine | Rerun test |
| Genuine | High confidence genuine, code-related | Escalate to code owner |
| Infrastructure | High confidence infra, transient | Check infrastructure, rerun |
| Abstain | Confidence too low or mixed signals | Manual engineer investigation |
