# AI Ledger: Phase 01 — Proposal Rejected

## Rejected Proposal: Accuracy Minimization

**Proposal:** Use accuracy (% correct predictions) as the objective. Three outputs, minimize error rate.

**Why it was plausible:** Accuracy is the standard ML metric. Simpler than cost-aware metrics.

**Why rejected for this context:**
- Accuracy treats all errors equally: 1 false positive = 1 false negative = 1 unit of error
- In this domain, errors are not equal:
  - Predicting genuine when actually flaky: cost 600 (time waste)
  - Predicting flaky when actually genuine: cost 5000 (ship broken code)
- An "accurate" system that minimizes errors equally could:
  - Predict "flaky" 80% of the time (high accuracy on the flaky-majority cases)
  - Occasionally miss genuine defects (1 miss = 5000 cost)
  - Overall accuracy = 95%, but catastrophic failure on the high-cost case

**What we use instead:**
- Cost minimization: minimize expected cost = Σ(P(true_cause) × cost(prediction, true_cause))
- Abstain option: allows the system to refuse low-confidence predictions rather than guess catastrophically
- Asymmetric cost matrix: reflects the asymmetric risk (5000 >> 600)

**Builder's decision:** Four outputs (flaky, genuine, infra, abstain); asymmetric cost matrix; objective is cost minimization, not accuracy.
