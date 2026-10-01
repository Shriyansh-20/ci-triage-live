# Knowns: Phase 00

| Evidence | Source | Status |
|----------|--------|--------|
| On-call engineer is the decision-maker at test failure | Working agreement (phase 00 conversation) | Confirmed |
| Decision window: ~6 hours (02:47 to 09:00 release) | Scenario (phase 00 TASK.md) | Known constraint |
| Three root cause categories exist: flaky, genuine, infra | Engineer's action tree (phase 00 conversation) | Assumed exhaustive |
| Cost matrix asymmetry: false negative (genuine→flaky) = 5000 | Cost analysis (phase 00 conversation) | Quantified |
| System emits probabilities, not decisions | Design boundary (phase 00 design) | Design choice |
| Test failure report is identical regardless of root cause | Scenario (phase 00 README) | Key problem statement |

## Uncertainties

- How are "flaky," "genuine," and "infra" operationally defined in the real CI logs?
- What data sources are actually available (logs, git history, metrics) at 02:47?
- Is there a baseline rate for each root cause in historical failures?
- How should the system handle edge cases (e.g., multiple tests failing)?
