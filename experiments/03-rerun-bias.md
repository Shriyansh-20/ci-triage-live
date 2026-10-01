# Experiment Design: Rerun Bias (Phase 03)

## Claim (Hypothesis)

**The "not-flaky" class is contaminated with hidden flakies.** 

When a test passes 10,000 times in a row (label = "not-flaky"), we cannot rule out that it will eventually flake on run 10,001 or 10,100. The rerun procedure **asymmetrically proves flakiness** (both pass and fail = proof) **but only disproves it weakly** (all pass = "we didn't see it fail in 10k tries").

**Direction of bias:** The "not-flaky" class contains false negatives—tests mislabeled as not-flaky that are actually flaky but rare (p_flake < 1/10000).

## Why This Matters for Evaluation

If the negative class (not-flaky, mixing genuine and infra) contains hidden flakies:

1. **Recall on "genuine" will be inflated.** When we train a model and evaluate on these labels, any prediction of "genuine" that lands on a hidden-flaky test appears correct (matches the label), but it's actually wrong (the test is really flaky).

2. **Precision on "flaky" will be artificially good.** Tests we correctly predict as flaky have clear evidence (they actually flaked during labeling). Tests we predict as flaky that were labelled "not-flaky" appear to be false positives, but some are actually true positives (hidden flakies mislabeled).

3. **Cost-weighted risk will underestimate the true cost.** Missing a hidden flaky (predicting "not flaky" when it's actually flaky) looks like a correct prediction in metrics, but in production it costs 5000 (broken code ships).

## Validation Strategy

We cannot fully validate this claim without observing hidden flakies (they're hidden by definition). But we can:

1. **Check stratification:** Collect tests with different rerun budgets (100, 1000, 10000). Predict all of them; see if tests with lower budget have higher predicted-flaky scores despite being labeled "not-flaky".
2. **Monitor production:** After deploying a triage model, track whether any "not-flaky" predictions actually flake in production.
3. **Sensitivity analysis:** Evaluate model performance assuming different contamination rates (1%, 5%, 10% of "not-flaky" are actually flaky) and see how metrics change.

## What Must Change in Evaluation

**Do not trust recall on genuine without knowing the rerun provenance.**

In phase 05 (evaluation), we must:
- Filter evaluation to only tests with sufficient rerun budget (e.g., >= 10,000 reruns)
- OR adjust recall calculation to account for known contamination rate
- OR track predicted flakiness separately for low-budget labels to expose the bias

This constraint carries forward to all downstream phases.
