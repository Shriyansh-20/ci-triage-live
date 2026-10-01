# Design: Evaluation Component (Phase 02)

## Responsibility

Measure system performance on triage predictions using a cost-aware metric ladder independent of any specific model or inference strategy.

## Reads

- Predicted probabilities (for flaky, genuine, infrastructure) or hard predictions
- Ground truth labels (actual root cause)
- Cost matrix from phase 01

## Emits

A set of diagnostics:
- **Cost-weighted risk** (primary objective)
- **Calibration metrics** (ECE with equal-width and equal-frequency bins, Brier score)
- **Class-level metrics** (precision, recall, F1 per class)
- **Coverage and risk-coverage** (what % of cases the system decides vs. abstains)
- **ROC AUC** (ranking quality)
- **Accuracy** (as a baseline, not the objective)

## Refuses

This component does **not**:
- Train or fit any model
- Tune hyperparameters
- Make decisions about which model is better (it only measures; humans decide)
- Modify predictions
- Report metrics that hide the asymmetric cost structure

## Constraint

Metrics must be computable from (true_label, predicted_proba) or (true_label, prediction) alone, independent of model internals.

## Connects To

**Input sources:** Model predictions, ground truth labels, cost matrix  
**Output consumers:** Model comparison, threshold tuning, diagnostic analysis  
**Downstream:** Phase 03+ model selection and improvement decisions
