# Design: Data Ingestion Layer (Phase 04)

## Responsibility

Load test metadata and test run history, join them, apply leak guard, emit clean feature matrix.

## Reads

- Test metadata CSV (one row per test: test_id, project, metadata)
- Test run history CSV (one row per run: test_id, outcome, timestamp, duration, etc.)
- Configuration: which columns are features vs. labels

## Emits

A DataFrame with one row per test run:
- Columns: features (safe to use for training)
- Column: label (ground truth for training)
- Columns: drop (metadata for analysis but not features; removed before model training)

## Refuses

This system does **not**:
- Emit columns that leak the label (computed from pass/fail history)
- Emit columns assuming future information (not in the dataset)
- Allow bypass of leak guard (guard is inside the loader, not optional)
- Modify the original CSVs (immutable inputs)

## Constraint

**Leak guard must be inside the loader function.** If it is optional, it will be skipped.

## Connects To

**Input sources:** FlakeFlagger CSVs (metadata, runs)  
**Output consumers:** Evaluation (phase 05+), model training (phase 07+)  
**Downstream:** Features and labels fed to split (phase 06), observers (phase 08+)
