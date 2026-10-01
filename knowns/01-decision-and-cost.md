# Knowns: Phase 01 — Output Space and Costs

## Cost Matrix (Confirmed)

| True Cause | System Output | Cost | Reason |
|-----------|---------------|------|--------|
| Flaky | Flaky | 0 | Correct |
| Genuine | Genuine | 0 | Correct |
| Infrastructure | Infrastructure | 0 | Correct |
| — | Abstain | 700 | Engineer manual investigation |
| Flaky | Genuine | 600 | Escalate unnecessarily, time waste |
| Flaky | Infrastructure | 400 | Time waste on infra check |
| Genuine | Flaky | **5000** | Ship broken code to production |
| Genuine | Infrastructure | 400 | Time waste, wrong investigation |
| Infrastructure | Flaky | 400 | Test rerun, time waste |
| Infrastructure | Genuine | 600 | Escalate engineer, time waste |

## Key Properties

1. **Matrix is asymmetric:** False negative on genuine (5000) >> all other errors (400-700)
2. **Abstain cost (700):** Cheaper than wrong prediction in most cases, especially the catastrophic case
3. **Objective:** Minimize expected cost (not accuracy)
4. **Trade-off:** System prefers to abstain (700) rather than guess genuinely (5000)

## Evidence

- Cost matrix from builder's phase 00 and 01 conversations
- Abstain output introduced when engineer fallback = manual logs investigation (~700)
- Costs are builder's estimates; not yet empirically validated

## Uncertainties

- True baseline rates for each cause in historical failures (affects expected cost calculation)
- Actual time cost of engineer manual investigation (estimated 700; could be 500-1000)
- Confidence threshold for abstention (not yet defined)
- Interaction between multiple failing tests (does cost change?)
