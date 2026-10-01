# AI Ledger: Phase 04 — Proposal Rejected

## Rejected Proposal: "Load All Columns, Drop Leakage Later"

**Proposal:** Load the full dataset without filtering. Let downstream code (model training, evaluation) decide which columns to drop. Simpler loader, more flexibility.

**Why it was plausible:**
- Loader could be simpler (just join and return)
- Downstream code has more visibility into which columns they use
- Easier to experiment with different feature sets

**Why rejected for this context:**
1. **Leak guard must be mandatory:** If leak removal is optional, someone will forget to call it. The leak becomes invisible until the model ships with perfect-looking performance.
2. **Design smell:** If the loader doesn't enforce safety, the contract is broken. Phase 04 design says: "Leak guard must be inside the loader, not optional."
3. **Outliability of the test fails:** The test `test_leak_guard_catches_label_derived_columns` is designed to outlive models. It only works if the guard is in the loader. Moving it to downstream code makes the test unfixable.
4. **Specific bug pattern:** This lab intentionally warns: "One of them is computed from the label. If you build a model before you find it, you will get a magnificent number and learn nothing at all." The only reliable way to prevent this is guard-in-loader.

**What we use instead:**
- Leak guard is **inside** `load_data()` function
- Guard checks for known leakage columns and drops them automatically
- Downstream code receives only safe features + label
- Test `test_leak_guard_catches_label_derived_columns` **fails** if leakage column reappears, outliving every model version

**Builder's decision:** Leak guard is mandatory and automatic, not optional. Loader owns the contract.
