# Knowns: Phase 03 — Ground Truth

## Label Procedure (Confirmed)

| Step | Confirmed |
|------|-----------|
| Rerun test on identical code, same environment | Yes |
| Stop early if both pass_count > 0 AND fail_count > 0 | Yes (flaky) |
| Rerun budget: up to 10,000 per test | Yes (builder decision) |
| Early stopping saves cost: flaky tests exit early | Yes |
| If budget exhausted without flip: label = "not-flaky" | Yes |
| Record provenance: reruns_executed, pass/fail counts, early_stop flag | Yes |

## Asymmetry (Confirmed)

| Outcome | Proves | Confidence |
|---------|--------|-----------|
| Both pass AND fail observed | Test is flaky. Definite. | High ✓ |
| All pass (N reruns) | "Might not be flaky." Rare flakiness possible. | Low ✗ |
| All fail (N reruns) | "Might be genuine/infra." Consistent failure, possible infrastructure. | Low ✗ |

**Direction of contamination:** "Not-flaky" class contains false negatives (hidden flakies) due to weak disproof.

## Cost Estimate

- Cost per run: 5 CI minutes (builder estimate)
- Per-test cost with early stop: ~250 minutes (flaky) to 50,000 minutes (not-flaky, full budget)
- For 1,000-test suite: expensive, justifies early stopping

## Rerun Bias Claimed (Phase 03 Experiment)

**Hypothesis:** "Not-flaky" class is contaminated with hidden flakies (tests that flake, but rarely, p < 1/10,000).

**Impact:**
- Recall on genuine inflated (hidden flakies look correctly predicted as "genuine")
- Precision on flaky artificially good (high signal from truly-flaky tests)
- Cost-weighted risk underestimated (hidden flakies hidden from evaluation)

**Validation in phase 05+:** Must stratify evaluation by rerun budget or filter to high-confidence labels only.

## Evidence

- Label procedure written with early stopping rule (builder conversation phase 03)
- Asymmetry analyzed: flaky proof vs. not-flaky weak disproof (builder feedback)
- Cost calculated: 5 min × 10,000 reruns = 50,000 min per test
- Rerun bias hypothesis stated (experiments/03-rerun-bias.md)

## Uncertainties

- True contamination rate of "not-flaky" class (unknown without observation of hidden flakies)
- What rerun budget is "enough"? (currently 10,000; could vary by test complexity)
- Will production data confirm the bias? (validation needed post-deployment)
- How to handle tests with heterogeneous rerun budgets? (stratification strategy TBD in phase 05)
- Interaction with infrastructure issues: all-fail outcome may indicate infra problem, not genuine bug

## Constraints for Downstream Phases

1. **Phase 05 (evaluation):** Cannot trust recall on genuine without provenance filtering
2. **Phase 07 (model training):** Must either filter low-budget labels or adjust loss to account for contamination
3. **Phase 13 (handoff):** Document hidden-flaky contamination in model caveats
