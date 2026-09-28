# Validation

Validation has two layers: automated evidence produced by the agent and final manual validation owned by a human. Test selection is governed by `TEST_STRATEGY.md`; security and performance checks are governed by `SECURITY.md` and `PERFORMANCE.md`.

## Automated validation

Derive applicable checks from the Profile, project rules, repository scripts/configuration, issue requirements, and changed surfaces. Do not hardcode commands.

Possible categories include every applicable family from `TEST_STRATEGY.md`: functional/behavioral, regression, negative/boundary, robustness, security, performance/reliability, compatibility/accessibility, migration/data, install/upgrade/rollback, static/build-time checks, and repository-specific quality gates. The taxonomy is comprehensive for consideration, not a requirement to execute irrelevant tests.

For each check record:

- command/action;
- why it applies;
- result: pass/fail/unavailable/not_applicable;
- concise evidence;
- for skipped categories, whether they are `not_applicable` or `unavailable` and why.

Never report `pass` without actual execution/observation.

## Validation cadence and evidence freshness

Order validation by information value, risk, and cost rather than running every check after every edit.

- During implementation, prefer the cheapest focused checks that can detect a regression in the changed slice.
- After a material increment, run the related checks whose inputs changed.
- Before `In Review`, run the full set of applicable release/review checks required by project evidence and the issue risk.
- Expensive integration, system, end-to-end, security, performance, load, or recovery checks belong at the earliest point where their additional fidelity is justified; do not run them repeatedly as reassurance.
- A previous green result remains reusable only while the command/check definition and its materially relevant inputs (code, configuration, dependencies, environment assumptions, test data/contracts) have not changed enough to invalidate it.
- When relevant inputs change, the prior result is stale and must not be presented as current evidence.
- Do not repeat an unchanged green command solely to increase confidence; repeated execution without new inputs usually adds no information.
- Failures and suspected flakes are different: investigate them according to their evidence rather than suppressing reruns categorically.

This cadence optimizes feedback without reducing final validation depth.

## Reporting validation evidence

Preserve complete validation evidence, but compress routine presentation:

- Detailed command/action, rationale, result, and evidence belong in the execution/validation artifact or equivalent durable record when available.
- In chat, group routine successful checks into a compact summary instead of narrating each one.
- Multiple `not_applicable` categories may be grouped with a shared rationale when accurate.
- Never collapse `unavailable` into `not_applicable` or `pass`; surface each material unavailable capability/reason needed for risk decisions.
- Expand failures, suspected flakes, security/performance regressions, unexpected results, residual risks, and checks that require human attention.
- When a failed check produces diagnostic artifacts, preserve/reference the useful artifacts when safe instead of discarding them or replacing them with an unsupported textual guess.
- Do not repeat the full manual validation plan in chat after saving it; provide its location plus the first human action or the specific decision required.
- Token/output reduction is never a reason to omit material evidence, uncertainty, a release blocker, or a required human gate.

## Evidence-backed diff review

Before entering `In Review`, review the changed surfaces against the issue, acceptance criteria, impact reconnaissance, and surrounding contracts/tests.

Only report a review finding when there is enough evidence to state:

- the concrete affected location/surface;
- a plausible failure/risk mechanism;
- supporting repository/test/runtime evidence;
- a severity justified by impact and likelihood rather than by a need to produce findings.

A clean review may legitimately produce zero findings. Do not invent nits or inflate severity to make the review look productive.

For tests specifically, verify that materially changed behaviors/acceptance criteria have meaningful proof, that assertions could detect the relevant regression, and that risk-relevant equivalent paths were not silently left inconsistent.

## Quality-bar integrity review

If the diff changes the mechanisms that decide whether work is acceptable, review the **quality bar itself**, not only the application code.

Look for evidence such as:

- an established threshold/budget/severity being weakened;
- a required check being removed from the lifecycle or CI path;
- tests being skipped/deleted or materially weakened;
- assertions being removed/narrowed so the relevant defect could pass;
- new suppression, exclusion, ignore, allowlist, or bypass directives;
- unfinished stubs, placeholder implementations, or failure paths converted into silent success;
- new exceptions/waivers without the project-required rationale, owner, scope, or expiry.

These are findings only when the change actually reduces an established/required control or hides incomplete work. Do not flag legitimate project-rule changes merely because the configuration changed. When weakening is intentional and material, require explicit issue/project evidence and use the applicable human decision/risk gate rather than letting a failing implementation redefine its own bar.

### Baseline ratchets without invented targets

When trustworthy project evidence already establishes a measured baseline as a quality/performance guardrail but no future target is defined, a non-regression **ratchet** may preserve the current line: do not get materially worse, and accept improvement.

Do not silently turn an incidental measurement into a new standing project policy. A ratchet is valid only when the repository, approved project rules, issue requirement, or explicit human decision makes that baseline normative. Record measurement noise/tolerance only from project evidence; never invent a universal tolerance.

## Failure handling

- Fix failures introduced by the change before review.
- If a failure appears pre-existing, establish that with evidence when feasible and report it separately.
- Do not weaken or delete legitimate checks to obtain green output.
- If a required check cannot run because of environment/capability limitations, report the limitation and compensate with the strongest safe alternative.
- A known material security regression or established performance-budget violation introduced by the change is release-blocking unless the specific residual risk is explicitly accepted by a human.
- Do not use repeated reruns to launder a flaky failure into a pass; follow `TEST_STRATEGY.md`.

## Manual validation plan

Generate `.implement-issue/MANUAL_VALIDATION_PLAN.md` as part of the `In Review` handoff. It must be tailored to the issue and actual diff, not generic boilerplate.

Include when applicable:

1. **Objective** — what the human is proving.
2. **Prerequisites** — environment, role/permissions, seed/test data, services, feature flags.
3. **Setup** — exact preparation steps without secret values.
4. **Happy-path scenarios** — numbered actions and expected result after each meaningful step.
5. **Edge/error scenarios** — boundaries introduced or affected by the change.
6. **Regression checks** — nearby behavior most likely to break because of the diff.
7. **Security checks** — authorization, isolation, sensitive data, negative inputs, trust boundaries, or other changed security surfaces when relevant.
8. **Performance/reliability checks** — responsiveness, representative workload, resource behavior, concurrency, or budgets when relevant.
9. **Cross-surface/device/accessibility/compatibility checks** — only when relevant.
10. **Data/migration/recovery checks** — only when relevant.
11. **Observability/log checks** — only when relevant and safe; ensure sensitive data is not exposed.
12. **Cleanup/rollback of test data** — when manual testing creates state.
13. **Pass/fail recording** — a clear place for the human to report failure details.

Use exact UI labels/routes/commands from repository or issue evidence when known. If a value is unknown, say so instead of inventing it.

## Human result

- Pass → final human gate satisfied.
- Fail → capture failing step, actual result, environment details supplied by the human, then return to implementation.
- Not run/partial → stay in `In Review`.
