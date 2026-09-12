# Dataset Choice: Phase 04

## Candidates Evaluated

### Candidate 1: FlakeFlagger (Zenodo 4450723)

**Metadata:**
- Published by: Alshammari, Morris, Hilton & Bell (2021)
- Licence: CC-BY-4.0 (Attribution required)
- Paper: "Predicting Flakiness Without Rerunning Tests"
- Source: https://zenodo.org/record/4450723

**Obligations:**
- Attribute authorship in publications
- May use freely for research and commercial purposes
- May share results publicly

**Appropriateness for this lab:**
- ✓ Designed for flaky-test classification research
- ✓ Public, reproducible, traceable
- ✓ Clear ground truth (tests labelled flaky/not-flaky)
- ✓ Compatible with phase 00-03 decisions (test failure triage)

### Candidate 2: IDoFT Dataset

**Metadata:**
- Published by: Amen et al.
- Licence: Restricted (unclear or proprietary restrictions)

**Obligations:**
- Academic use only (cannot publish results without permission)
- OR unclear provenance/licence

**Appropriateness for this lab:**
- ✗ Licence restricts publication
- ✗ Cannot share findings if using this data
- ✗ Not compatible with open-source/reproducible research goals

## Decision: Use FlakeFlagger

**Why FlakeFlagger wins:**
1. **Clear licence (CC-BY-4.0):** Can use, share, publish findings
2. **Published research data:** Transparent provenance, peer-reviewed context
3. **Designed for exactly this problem:** Flaky test classification
4. **No downstream restrictions:** Results can be shared, reproduced, extended

**Why IDoFT is rejected:**
- Licence restrictions block publication of results
- Cannot share trained models or findings without permission
- Reduces reproducibility and scientific value

## Data Structure (FlakeFlagger)

Based on the Alshammari et al. paper and typical research dataset structure:

**Two input files:**
1. Test metadata CSV: one row per test (test_id, project_id, class, method, features)
2. Test runs CSV: one row per run (test_id, build_id, outcome, timestamp, duration)

**Join:** On `test_id`

**Output:** One row per test run, with features + label (outcome)

## Licence Compliance

- Download from Zenodo with attribution
- Record in PROBLEM.md or README: "Data from FlakeFlagger (Zenodo 4450723, CC-BY-4.0)"
- Include citation: Alshammari, Morris, Hilton & Bell (2021)
