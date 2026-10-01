# AI Ledger: Phase 03 — Proposal Rejected

## Rejected Proposal: Ignore Rerun Provenance

**Proposal:** Record only the final label (flaky | not-flaky). Don't track how many reruns, early stop status, or pass/fail counts. Simpler data, simpler evaluation.

**Why it was plausible:**
- Simpler dataset schema (one column: label)
- Faster to evaluate (no need to filter by provenance)
- Labels are labels; the past doesn't matter

**Why rejected for this context:**
1. **Contamination is unquantifiable:** Without provenance, you cannot measure or adjust for label contamination. A "not-flaky" label from 50 reruns is very different from one from 10,000 reruns, but they'd be treated identically.
2. **Bias hidden in metrics:** With full provenance visible, you can stratify evaluation and see: "our model's recall on 10k-rerun tests is 95%, but on 100-rerun tests is only 60%." Without provenance, you'd only see a blended 75% and miss the hidden flakies.
3. **Production risk masked:** Tests labeled "not-flaky" after only 100 reruns have high hidden-flaky contamination. Without provenance, you deploy confidently and ship bugs.
4. **Future engineer cannot discount:** Phase 03 README says: "What must the system record so a future engineer can discount the label correctly?" With no provenance, future engineers have no way to adjust or doubt the labels.

**What we use instead:**
- Full provenance: label, reruns_executed, early_stop, pass_count, fail_count
- Label confidence tied to provenance (10,000 reruns = more confident than 100)
- Evaluation must stratify or filter by provenance
- Hidden flaky bias explicitly acknowledged and tracked

**Builder's decision:** Every label includes its provenance. Ground-truth component emits label + metadata. Evaluation cannot trust "not-flaky" without knowing the rerun budget.
