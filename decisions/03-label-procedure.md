# Label Procedure: Phase 03

## The Mechanism

For each test failure, execute the following procedure:

### Input
- Test failure: (test_name, code_revision, environment)
- Rerun budget: up to N reruns (starting with N=10,000)
- Risk stratification: optional (can reduce N for low-risk cases)

### Algorithm
1. **Initialize:** pass_count = 0, fail_count = 0, reruns_done = 0
2. **Loop:** While reruns_done < N:
   - Run test on identical code, same environment
   - Increment reruns_done
   - If outcome == pass: pass_count++
   - If outcome == fail: fail_count++
   - **Early stop condition:** If (pass_count > 0 AND fail_count > 0), stop immediately
3. **Assign label:**
   - If (pass_count > 0 AND fail_count > 0): **label = flaky**
   - Else: **label = not-flaky**
4. **Record provenance:**
   - early_stop = (pass_count > 0 AND fail_count > 0)
   - Emit: (test_name, label, reruns_done, pass_count, fail_count, early_stop, cost_ci_minutes)

## What Each Outcome Proves

| Outcome | Proves |
|---------|--------|
| Both pass_count > 0 AND fail_count > 0 | **Definite flaky.** Test can both succeed and fail on identical code. Proof is conclusive. |
| pass_count == N (all passes) | **"Might be genuine or infra."** Did not observe failure in N attempts, but cannot rule out rare flakiness. Label confidence is low. |
| fail_count == N (all failures) | **"Might be genuine or infra."** Consistently fails (probably genuine bug), but infrastructure issue is possible. Label confidence is low. |

## Early Stopping Saves Cost

- Without early stop: every test runs the full budget (expensive)
- With early stop: flaky tests identified early, no wasted reruns
- Example: test that flakes on run 50 exits immediately; saves 9,950 reruns
- For a true not-flaky test, pays full cost (N reruns) to earn confidence

## Cost Calculation

Cost per label = reruns_executed × cost_per_run (CI minutes)

Example:
- Cost per run = 5 minutes
- Flaky test (early stop at 50): 50 × 5 = 250 minutes
- Not-flaky test (full 10k): 10,000 × 5 = 50,000 minutes

Multiplied across 1,000 tests: expensive.
