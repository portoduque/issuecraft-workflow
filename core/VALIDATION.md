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

## Reporting validation evidence

Preserve complete validation evidence, but compress routine presentation:

- Detailed command/action, rationale, result, and evidence belong in the execution/validation artifact or equivalent durable record when available.
- In chat, group routine successful checks into a compact summary instead of narrating each one.
- Multiple `not_applicable` categories may be grouped with a shared rationale when accurate.
- Never collapse `unavailable` into `not_applicable` or `pass`; surface each material unavailable capability/reason needed for risk decisions.
- Expand failures, suspected flakes, security/performance regressions, unexpected results, residual risks, and checks that require human attention.
- Do not repeat the full manual validation plan in chat after saving it; provide its location plus the first human action or the specific decision required.
- Token/output reduction is never a reason to omit material evidence, uncertainty, a release blocker, or a required human gate.

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
