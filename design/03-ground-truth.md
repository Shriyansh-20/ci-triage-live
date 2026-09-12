# Design: Ground-Truth Source (Phase 03)

## Responsibility

Produce and record durable labels for test failure root cause with full provenance (how the label was generated, at what confidence).

## Reads

- Test failure records (which test failed, code revision, environment)
- Rerun budget and stopping criteria
- Risk stratification (if applied)

## Emits

A label record per test:
- **label** (flaky | not-flaky)
- **reruns_executed** (integer, 1 to N)
- **early_stop** (boolean)
- **pass_count, fail_count** (observed outcomes)
- **cost_ci_minutes** (compute cost for this label)

## Refuses

This system does **not**:
- Predict the cause itself (labels what to train on, not predictions)
- Decide how many reruns are "enough" (builder sets stopping rule)
- Discard low-confidence labels (records them with provenance instead)
- Make decisions about deployment (label is input to downstream phases)

## Constraint

Every label must include its provenance (reruns, outcomes). A label with no sample size is useless.

## Connects To

**Input sources:** CI failure reports, test code, execution logs  
**Output consumers:** Evaluation (phase 02+), model training (phase 07+)  
**Depends on:** Cost per CI minute, stopping rule, rerun budget strategy
