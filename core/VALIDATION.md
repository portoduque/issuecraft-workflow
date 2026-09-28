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

### Probe before `unavailable`

An applicable check should be labeled `unavailable` only after proportionate evidence establishes the limitation. Prefer one of:

- a safe execution attempt and its observed failure;
- a safe prerequisite/capability probe;
- direct environment/project evidence that the required capability or dependency is unavailable.

A narrative assumption such as "the environment probably cannot run this" is not enough. Do not perform a destructive, production-impacting, externally mutating, or expensive/high-load action merely to prove unavailability; in those cases, use the strongest safe prerequisite/capability evidence available.

### Partial evidence is not full verification

Evidence can support part of an obligation without proving the whole obligation. Preserve that distinction.

- If a multi-part requirement has six material members and only four are proven, report four proven and two unverified; do not upgrade the parent obligation to `pass`.
- A readable subset of artifacts, tests, environments, paths, roles, or cases does not make the missing subset pass.
- Continue validating whatever evidence is available, but label the unsupported portion explicitly.
- An overall `pass` requires evidence for every material applicable member, except members correctly classified `not_applicable`.

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

### Integration freshness before In Review

When the repository/VCS can identify an integration baseline/current base, check whether that base materially changed while the issue was in progress before entering `In Review`.

- If the base did not change, keep current evidence.
- If the base changed only on surfaces that cannot materially affect this issue's changed behavior, contracts, dependencies, build/test definitions, or risk assumptions, do not rerun unrelated green checks merely because another issue merged.
- If the base changed a materially relevant surface, reconcile according to the project's integration policy, re-evaluate the affected diff/contracts, mark only dependent validation evidence stale, and rerun the checks whose inputs changed.
- Do not perform an automatic rebase/merge solely because the base moved; branch/integration policy belongs to the project/environment.
- If freshness cannot be established and the uncertainty is material to release safety, report the limitation instead of pretending prior evidence is current.

The goal is selective invalidation, not full revalidation after every unrelated parallel change.

## Reporting validation evidence

Preserve complete validation evidence, but compress routine presentation. **Compact output must be a projection of the complete validation result, never a reduced validation scope.** The same applicable checks, material obligations, verdicts, failures, unavailable checks, and risk decisions must exist before presentation is compressed:

- Detailed command/action, rationale, result, and evidence belong in the execution/validation artifact or equivalent durable record when available.
- In chat, group routine successful checks into a compact summary instead of narrating each one.
- For verbose logs/test output, surface the decisive result, material counts/status, and the shortest useful failure/error/location evidence; preserve or reference the complete diagnostic artifact when available instead of dumping routine noise into chat.
- Multiple `not_applicable` categories may be grouped with a shared rationale when accurate.
- Never collapse `unavailable` into `not_applicable` or `pass`; surface each material unavailable capability/reason needed for risk decisions.
- Expand failures, suspected flakes, security/performance regressions, unexpected results, residual risks, and checks that require human attention.
- When a failed check produces diagnostic artifacts, preserve/reference the useful artifacts when safe instead of discarding them or replacing them with an unsupported textual guess.
- Do not repeat the full manual validation plan in chat after saving it; provide its location plus the first human action or the specific decision required.
- Token/output reduction is never a reason to omit material evidence, uncertainty, a release blocker, or a required human gate.
- Compact presentation must preserve material semantic qualifiers and exact decision-bearing data; a shorter statement that changes meaning is a validation/reporting defect, not an efficiency gain.

## Evidence-backed diff review

Before entering `In Review`, review the changed surfaces against the issue, acceptance criteria, impact reconnaissance, and surrounding contracts/tests.

Every **material diff change needs justification traceability** to at least one legitimate source: issue/acceptance requirement, established repository/project invariant, security/performance/reliability/compatibility obligation, or a necessary enabling change for one of those. Unjustified material change is a scope/coherence concern, not free cleanup.

Only report a review finding when there is enough evidence to state:

- the concrete affected location/surface;
- a plausible failure/risk mechanism;
- supporting repository/test/runtime evidence;
- a severity justified by impact and likelihood rather than by a need to produce findings;
- a specific corrective action when the evidence makes one known.

A clean review may legitimately produce zero findings. Do not invent nits or inflate severity to make the review look productive.

### Solution-economy / ownership review

After correctness/completeness and applicable proof obligations are satisfied, inspect whether the diff introduces avoidable ownership or speculative complexity.

Look for evidence-backed cases such as:

- a new abstraction, wrapper, extension point, configuration layer, dependency, file/module, or custom implementation when an adequate established project/runtime/platform capability already covers the requirement;
- duplicated project behavior or validation that should reuse an existing source of truth;
- indirection that adds no material contract, isolation, reuse, compatibility, or risk-control value;
- future-proofing for hypothetical variants with no issue/project evidence.

Do **not** use raw LOC, file count, deletion count, or dependency count as quality scores. Necessary boundaries and explicit requirements are not over-engineering merely because they add code. Solution economy is secondary to the proof floor: correctness, completeness, preservation, security, performance/reliability, accessibility, compatibility, and required validation remain controlling.

When a simpler design is chosen with a material known operational ceiling, ensure the ceiling and evidence-based revisit trigger are recorded. Do not manufacture debt records for ordinary simple code.

### Behavior-delta verification

When the issue materially changes behavior or a contract, verify the resulting state according to the delta semantics established during planning:

- **added** — the new behavior exists and its material scenarios/obligations are proven;
- **modified** — the requested new behavior is proven **and preservation obligations remain intact**; do not let a partial rewrite silently erase existing scenarios, fields, states, roles, compatibility behavior, or error paths that were not explicitly removed;
- **removed** — the old behavior is no longer delivered where removal is required; finding no implementation is expected, not a reason to re-add it;
- **renamed/preserved** — the semantic behavior remains; do not require internal code-symbol/file renames unless they are part of the actual contract;
- **unchanged-but-at-risk** — nearby behavior exposed to regression by the diff remains intact with proportionate evidence.

When the baseline cannot be established from evidence, report the relevant preservation/delta claim as unverified rather than inventing what used to be true.

### Change coherence review

Before `In Review`, reconcile the whole change as one contract:

1. issue intent and acceptance criteria;
2. applicable project/repository contracts and rules;
3. current-contract -> requested-delta -> resulting-contract model when applicable;
4. implementation diff;
5. automated test/validation evidence;
6. issue-specific manual validation plan.

Look for contradictions in **any direction**, including code that implements behavior the issue did not authorize, tests that prove a different outcome than the issue requires, accepted behavior omitted from the diff, preservation obligations lost during a modification, or a manual plan that fails to exercise a material changed risk.

A plan is not authoritative merely because it was written earlier. Current issue/project contracts plus repository evidence control; revise local/reversible plan assumptions when they are disproven. Material issue-intent/scope changes remain human decisions.

For tests specifically, apply the evidence rules from `TEST_STRATEGY.md`:

- use **evidence-or-zero**: a material obligation is not covered unless concrete evidence identifies what proves the required outcome;
- decompose compound/enumerated requirements so one broad assertion does not hide an unproven field, case, state, role, or clause;
- record verification precision gaps rather than inventing expected values;
- when risk/uncertainty justifies it, use a safe isolated discrimination check to prove that the relevant test/check can actually detect the wrong behavior;
- verify that risk-relevant equivalent paths were not silently left inconsistent.

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

## Approval freshness for gated actions

For an action that required a human gate, validate approval freshness immediately before execution rather than treating earlier conversational approval as permanently valid.

- Compare the current target/environment, material scope/effects, known risk, and gate-relevant preconditions with what the human reviewed.
- If they remain substantively equivalent, the approval remains usable; incidental reversible mechanics do not require another approval.
- If a material difference would change what a reasonable reviewer understood they were authorizing, mark the prior approval stale, surface the delta, and obtain fresh approval.
- Do not let replanning, recovery, rollback, cleanup, retries, or follow-up work silently widen a previous authorization.
- This is a semantic integrity check, not a requirement for hashes, persistent plan artifacts, or a new approval gate on routine implementation work.

## Failure handling

- Fix failures introduced by the change before review.
- If a failure appears pre-existing, establish that with evidence when feasible and report it separately.
- Do not weaken or delete legitimate checks to obtain green output.
- If a required check cannot run because of environment/capability limitations, apply the safe probe-before-`unavailable` rule, report the limitation, and compensate with the strongest safe alternative.
- A known material security regression or established performance-budget violation introduced by the change is release-blocking unless the specific residual risk is explicitly accepted by a human.
- Do not use repeated reruns to launder a flaky failure into a pass; follow `TEST_STRATEGY.md`.

## Manual validation plan

Generate `.implement-issue/issues/<issue-key>/MANUAL_VALIDATION_PLAN.md` as part of the `In Review` handoff. It must be tailored to the issue and actual diff, not generic boilerplate. One issue's plan must not replace another issue's plan.

For backward compatibility, a legacy root-level `.implement-issue/MANUAL_VALIDATION_PLAN.md` may be consulted only when its issue identity unambiguously matches the current issue. New/updated plans use the issue-scoped path; do not delete an ambiguous legacy plan automatically.

Include when applicable:

1. **Objective** — what the human is proving.
2. **Prerequisites** — environment, role/permissions, seed/test data, services, feature flags.
3. **Setup** — exact preparation steps without secret values.
4. **Happy-path scenarios** — numbered actions and expected result after each meaningful step.
5. **Edge/error scenarios** — boundaries introduced or affected by the change.
6. **Regression/preservation checks** — nearby behavior most likely to break because of the diff, including unchanged obligations on a modified surface that the issue did not authorize removing.
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
