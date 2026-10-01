# Knowns: Phase 04 — Data and Licence

## Dataset Choice (Confirmed)

| Candidate | Licence | Usable | Notes |
|-----------|---------|--------|-------|
| FlakeFlagger (Zenodo 4450723) | CC-BY-4.0 | ✓ YES | Published, attribute required, results sharable |
| IDoFT | Restricted | ✗ NO | Licence blocks publication of results |

**Selected: FlakeFlagger**
- Published: Alshammari, Morris, Hilton & Bell (2021)
- Paper: "Predicting Flakiness Without Rerunning Tests"
- Licence: CC-BY-4.0 (Attribution required, otherwise free to use)

## Data Structure (Expected)

**Two input files:**
1. Test metadata: one row per test (test_id, project_id, class, method, features)
2. Test runs: one row per run (test_id, build_id, outcome, timestamp, duration)

**Join:** On `test_id` → one row per test run with features + label

## Leak Guard (Implemented)

**Location:** Inside `ci_triage/data.py::load_data()` function (mandatory, not optional)

**Leakage columns removed:**

| Column | Type | Why Removed |
|--------|------|-------------|
| flakiness_score | Label-derived | Computed from pass/fail history; perfect signal; no learning |
| failure_rate | Label-derived | Computed from outcomes; collinear with label |
| pass_rate | Label-derived | Computed from outcomes; collinear with label |
| coefficient_of_variance | Label-derived | Computed from pass/fail variance; leaked signal |
| times_flipped | Label-derived | Computed from transitions; leaked signal |
| future_passes_in_next_100_runs | Future info | Assumes data not yet observed; not available at decision time |

## Tests (Confirmed)

1. **test_leak_guard_catches_label_derived_columns:** PASSED
   - Creates toy data with `failure_rate` (leakage)
   - Calls `load_data()`
   - Asserts: `failure_rate` is removed
   - **Fails if guard is missing or bypassed**

2. **test_leak_guard_preserves_safe_columns:** PASSED
   - Verifies `duration`, `test_class` remain after leak removal
   - Ensures guard doesn't over-drop

3. **test_get_features_and_labels:** PASSED
   - Feature/label split works correctly

4. **test_exploratory_analysis:** PASSED
   - EDA computes rows, projects, labels, positive rate

5. **test_leakage_columns_list_not_empty:** PASSED
   - Sanity check: guard has something to guard

## Evidence

- Leak guard code in `ci_triage/data.py`: 75 lines, uses pandas
- Test suite: 5 tests, all passing
- Leak detection test explicitly designed to outlive models
- EDA placeholder ready for when data is downloaded
- Licence choice documented and justified

## Uncertainties

- Exact column names in FlakeFlagger CSV (will confirm on download)
- Additional leakage columns not yet in the known list (will discover in EDA)
- Missing value patterns (will analyze when data loaded)
- Project distribution and test coverage (will see in EDA)
- Whether all 2 files need to be joined or if pre-joined file exists (check Zenodo)

## Downstream Constraints

1. **Phase 05 (splits):** Must account for rerun provenance contamination from phase 03
2. **Phase 06 (baselines):** Constant predictor test should work on this data
3. **Phase 07+ (models):** Cannot use features dropped by leak guard; must only train on safe columns
