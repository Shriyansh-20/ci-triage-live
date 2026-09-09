# Metric Ladder: Phase 02

## Primary Objective

**Cost-weighted risk** — the expected cost of predictions given the cost matrix from phase 01.

## Why This Order

The ladder starts with cost-weighted risk (the question: how much does this system cost?) then diagnostics that explain why:

| Metric | Question | What It Catches |
|--------|----------|-----------------|
| **Cost-weighted risk** | What is the expected cost? | Overall performance on what matters |
| **Recall (genuine)** | Do we catch genuine defects? | Underestimation of genuine (5000 cost) |
| **Precision (genuine)** | When we say genuine, are we right? | False positives on genuine (600 cost) |
| **Coverage** | What % of cases do we decide vs. abstain? | Over-abstaining (hiding behind uncertainty) |
| **ECE (equal-width bins)** | How miscalibrated are probabilities? | Systematic over/underconfidence |
| **ECE (equal-frequency bins)** | Same, but fair to rare classes? | Class imbalance artifacts in calibration |
| **Brier score** | How far are predicted probabilities from reality? | Penalty for confident wrong answers |
| **ROC AUC** | How good is the ranking, ignoring threshold? | Baseline discrimination ability |
| **Accuracy** | % correct (hard predictions only) | Baseline; known to be misleading here |
| **Recall (flaky, infrastructure)** | Do we catch flaky/infra correctly? | Diagnostic: where else are we weak? |
| **Precision (flaky, infrastructure)** | False positives on flaky/infra? | Diagnostic: what's our false positive pattern? |

## Critical Insight: Why Not Just Accuracy?

A constant predictor ("always not flaky") scores ~94% accuracy on a 3% positive base rate but catches 0% of genuine defects (recall=0). 

The metric ladder exposes this:
- Accuracy: 94% ✓ (looks good!)
- Recall (genuine): 0% ✗ (we're missing the catastrophic cases)
- Cost-weighted risk: 5000 * 0.03 = 150 per case (disaster!)

## Calibration: Equal-Width vs. Equal-Frequency

**Equal-width bins:** Divides predicted probability into bins of equal width (e.g., [0-.1], [.1-.2], ..., [.9-1.0]).
- Problem: on rare classes (3% genuine), most bins will be empty
- Creates high ECE variance

**Equal-frequency bins:** Divides predictions into bins with equal count of samples.
- Better: ensures each bin has enough data to measure calibration
- More robust when base rates are imbalanced

For our 3% genuine base rate, equal-frequency binning will be less misleading.

## Cost-Weighted Risk Calculation

```
cost_weighted_risk = mean over all samples of:
    sum over all true causes of:
        P(true_cause) * cost(predicted, true_cause)
```

Direct translation of our phase 01 cost matrix into a scalar metric.
