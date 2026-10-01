# Design: System Boundary (Phase 00)

## Responsibility

Triage a test failure in the CI pipeline to determine root cause and guide the on-call engineer's decision about how to proceed before a 09:00 release.

## Reads

- Test failure signal from CI (test name, assertion, timestamp)
- CI logs and test output
- Git history of recent commits to the release branch
- Infrastructure/environment metadata (if available)

## Emits

Probability estimates for three root causes:
- Probability the test is **flaky** (fails randomly, not code-related)
- Probability the failure is **genuine** (code change caused it)
- Probability the failure is an **infrastructure issue** (transient, environmental)

## Refuses

This system does **not**:
- Make the decision to stop/proceed with the release
- Delete or skip the test
- Automatically merge, revert, or commit code
- Wake up or contact any engineer
- Modify the build pipeline or infrastructure
- Determine which engineer owns a failing test

## Constraint

Must produce a triage within the decision window (~6 hours, 02:47 to 09:00).

## Connects To

**Input sources:** CI system, git repository, logs  
**Output consumer:** On-call engineer (deployment decision-maker)  
**Subsequent phases:** Root cause analysis, remediation actions (outside this system's scope)
