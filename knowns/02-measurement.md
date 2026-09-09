# Knowns: Phase 02 — Measurement

## Metric Ladder (Confirmed)

| Metric | Primary? | Question | Implementation |
|--------|----------|----------|-----------------|
| Cost-weighted risk | ✓ YES | Expected cost of predictions | From phase 01 cost matrix |
| Recall (genuine) | ✓ YES | Do we catch genuine defects? | Diagnostic on class='genuine' |
| ECE (equal-frequency) | ✓ YES | How miscalibrated are probabilities? | Binned calibration error |
| Coverage | ✓ YES | What % decide vs. abstain? | 1 - (abstain_count / n_total) |
| Precision (genuine) | Diagnostic | False positives on genuine? | Per-class precision |
| Brier score | Diagnostic | Probability distance from truth | Squared error on probabilities |
| ROC AUC | Diagnostic | Ranking quality | Baseline discrimination |
| Accuracy | Baseline | % correct | Known to be misleading here |

## Tests (Confirmed)

1. **Constant predictor trap:** Accuracy=97%, recall(genuine)=0%, cost=150 (expensive!). Test validates that cost-weighted risk catches what accuracy hides.
2. **Calibration comparison:** Equal-width ECE vs. equal-frequency ECE on imbalanced data (3% genuine) show different behavior. Equal-frequency is more robust.
3. **Cost matrix applied correctly:** Cost lookup works for all 12 entries in cost matrix.
4. **Abstention cost:** Each abstain costs 700.
5. **Metrics return floats:** All metrics output floats, no exceptions.

## Code Artifacts

- `ci_triage/metrics.py` (~75 lines, uses sklearn): cost-weighted risk, ECE, precision/recall, coverage
- `tests/test_metrics.py` (~120 lines): 5 tests capturing the phase invariants (constant predictor trap, cost matrix, abstention, binning difference)

## Evidence

- Cost matrix from phase 01 correctly translates to code
- Test suite validates that constant predictor is exposed as bad on cost (150) despite good accuracy (97%)
- All five tests pass: constant trap, ECE binning, cost applied, abstention, and type validation

## Uncertainties

- True baseline rates for each root cause (will come from data in phase 03+)
- Actual performance of real models vs. constant predictor and toy data
- Whether ECE binning difference (equal-width vs. equal-frequency) matters on real data
- Threshold for abstention (not yet defined; depends on acceptable cost level)
- Interaction between multiple failing tests (single test in scope here)
