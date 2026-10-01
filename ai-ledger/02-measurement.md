# AI Ledger: Phase 02 — Proposal Rejected

## Rejected Proposal: Threshold-Based Approach (No Abstention)

**Proposal:** Don't build a separate evaluation component. Instead, apply a threshold to model probabilities: if max(P_flaky, P_genuine, P_infra) > 0.7, predict the argmax; otherwise don't predict anything.

**Why it was plausible:**
- Simpler than building a full metric ladder
- Threshold is interpretable
- Handles confidence naturally

**Why rejected for this context:**
1. **Metric confusion:** Threshold tuning requires knowing what metric you're optimizing. Without the cost matrix baked into the evaluation, you'd end up tuning on accuracy (the trap from the constant predictor).
2. **Cannot compare models fairly:** Different models might use different thresholding logic. One model embeds thresholding in its prediction; another uses a simple argmax. You cannot score them on identical terms.
3. **Cost-weighted risk hidden:** By putting threshold logic into the model, you lose the ability to see which errors are most expensive. The metric ladder exposes asymmetry; threshold logic obscures it.
4. **Diagnosis is impossible:** If cost-weighted risk is high, you want to know: is it because recall on genuine is low, or because ECE is bad? With threshold-in-the-model, you cannot separate model quality from threshold choice.

**What we use instead:**
- Separate evaluation component (this phase)
- Cost-weighted risk as primary metric
- Full diagnostic ladder (ECE, calibration, precision, recall per class)
- Abstain as a first-class output, not a side effect of thresholding

**Builder's decision:** Evaluation component is separate from any model. Metrics expose cost asymmetry. Abstain is intentional, not accidental.
