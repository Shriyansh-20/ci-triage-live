# Design: Output Space and Caller Contract (Phase 01)

## Responsibility

Emit a categorical decision on test failure root cause (or abstain when confidence is insufficient), such that the on-call engineer can take appropriate action with known cost trade-offs.

## Reads

- Triage signals from phase 00 (probabilities for flaky, genuine, infrastructure)
- Confidence threshold (decision boundary)

## Emits

One of four outputs:
1. **Flaky** — test fails randomly, unrelated to code changes
2. **Genuine** — test failure caused by a code change in this PR/commit
3. **Infrastructure** — failure due to transient environment/network issue
4. **Abstain** — system confidence too low; engineer must investigate manually

## Refuses

This system does **not**:
- Decide whether to stop/proceed with the release
- Contact any engineer or escalate automatically
- Determine the correct output when confidence is borderline (that's for abstention)
- Modify tests or code
- Change infrastructure

## Constraint

Must emit exactly one output (no hedging, no multiple outputs).

## Connects To

**Input:** Phase 00 probabilities  
**Output consumers:**  
  - Flaky → Engineer reruns test, proceeds if stable
  - Genuine → Engineer contacts code owner, may revert
  - Infrastructure → Engineer checks infrastructure, reruns
  - Abstain → Engineer manually reads logs and decides

**Downstream:** Engineer's action (rerun, escalate, check infra, or manual investigation)
