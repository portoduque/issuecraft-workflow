# Test Strategy

The workflow is test-framework agnostic and uses risk-based test selection. Every issue must consider the full semantic test taxonomy below, but it must run or add only the tests that are applicable to the changed behavior, project architecture, risk, and available infrastructure.

`not_applicable` is valid only with a reason. `unavailable` means the test is applicable but cannot currently be executed. Neither means `pass`.

## Test applicability matrix

During planning, evaluate each family below. Expand to individual types when the change makes them relevant. Reassess after the diff is complete.

For every selected type capture:

- why it applies;
- existing command/tool or test location when known;
- whether a new/updated test is needed;
- execution result: `pass`, `fail`, `unavailable`, or `not_applicable`;
- evidence.

Do not create a new foundational testing framework without an approved project decision when no applicable test infrastructure exists.

## Behavior-to-evidence traceability

Passing a large test suite is not enough by itself. For every materially changed behavior and acceptance criterion, identify the strongest applicable verification evidence.

Prefer the **lowest-cost test layer that can faithfully prove the behavior**. Escalate fidelity only when the risk depends on real subsystem interaction, persistence, runtime behavior, network boundaries, platform/browser behavior, cross-component contracts, or an assembled user/business journey.

A passing test is useful evidence only when its assertions materially discriminate correct behavior from the relevant failure. Prefer observable behavior, contracts, and invariants over implementation-detail assertions. A no-throw check or broad snapshot is not automatically meaningful evidence.

## Functional and behavioral tests

- **Unit** — isolated behavior of a small unit.
- **Component/module** — a larger unit with its internal collaborators as the project defines it.
- **Integration** — interaction between real subsystems/resources.
- **Contract** — producer/consumer or interface compatibility expectations.
- **API/interface** — externally observable interface behavior independent of UI.
- **System** — behavior of the assembled system in a representative environment.
- **End-to-end** — complete user/business flow through relevant layers.
- **Acceptance** — business/acceptance-criteria verification.
- **Smoke/sanity** — narrow proof that critical paths start and minimally work.
- **Regression** — behavior known to have worked or a bug that must not recur.
- **Exploratory/manual** — human investigation where automation is insufficient.

## Negative, robustness, and correctness tests

- error/failure-path tests;
- boundary/edge-case tests;
- state-transition tests;
- data-integrity/transaction tests;
- property-based/generative tests;
- fuzz tests;
- mutation tests for test-suite effectiveness when project infrastructure supports them;
- concurrency/race/locking/idempotency tests;
- resilience/retry/fallback/fault-injection/chaos tests where the architecture and safe environment make them appropriate.

## Security tests

Use `SECURITY.md` for security-impact analysis. Applicable test types can include:

- authentication/authorization/isolation tests;
- negative input/trust-boundary tests;
- security regression tests;
- static security checks;
- dependency/supply-chain checks;
- secret/configuration checks;
- safe fuzz/property tests;
- security-focused integration/E2E/manual scenarios.

## Performance and reliability tests

Use `PERFORMANCE.md` for impact analysis. Applicable test types can include:

- benchmark/microbenchmark;
- load;
- stress;
- spike;
- soak/endurance;
- scalability;
- resource/leak measurement;
- concurrency/contention;
- performance regression against an established baseline/budget.

## Compatibility and quality tests

When applicable, consider:

- accessibility;
- visual regression;
- cross-browser/device/platform/runtime compatibility;
- backward/forward compatibility;
- localization/internationalization;
- installation/packaging;
- upgrade/downgrade/rollback;
- migration/schema/data-conversion tests;
- backup/restore/recovery tests;
- generated-code/schema/artifact consistency;
- observability/telemetry behavior;
- CLI/help/error-output behavior;
- configuration compatibility.

## Static and build-time verification

These are verification gates even when they are not conventionally called tests:

- lint/style policy;
- formatting verification;
- type/static analysis;
- compile/build/package;
- architecture/dependency-boundary checks;
- schema/config validation;
- documentation/example compilation or doctests when applicable.

## Bug-fix regression rule

For a reproducible defect, prefer establishing a failing regression test or equivalent reproducible automated check before the fix when feasible. A reproducer counts as valid **RED evidence only when the failure is attributable to the targeted defect, missing behavior, or violated invariant**. Unrelated setup, syntax, dependency, environment, or pre-existing failures do not establish the defect.

After the fix:

- demonstrate that the reproducer passes;
- keep nearby relevant regression coverage green;
- when the root cause can plausibly affect equivalent paths or sibling surfaces, inspect and test the risk-relevant siblings rather than patching only the reported example.

Consider path parity when an invariant/interface has multiple implementations or modes, such as primary/fallback, enabled/disabled, success/rollback, cached/uncached, role/tenant variants, compatibility paths, or other repository-specific equivalents. Test only the variants supported by actual project evidence and risk.

Do not force test-first development when the repository has no such rule and a failing automated reproducer is unsafe/impractical; explain the alternative evidence instead.

## Flaky tests

Do not repeatedly rerun a failure until it turns green and then call it passing. A bounded rerun may be used to characterize nondeterminism, but the final report must distinguish stable pass, stable fail, and suspected flake with evidence.

When available, preserve useful failure artifacts such as traces, logs, screenshots, recordings, dumps, or reports. Prefer synchronization on observable conditions/invariants over arbitrary sleeps/time delays. Quarantining or skipping a known flaky check does not convert it into a pass; record the unresolved risk according to project policy.

## Coverage

Respect existing coverage requirements if present. Do not invent a global coverage percentage. Coverage is evidence about exercised code, not proof of correctness; prioritize risk-relevant assertions and behavior.

## Test doubles and boundary fidelity

Mocks, fakes, stubs, simulators, and sandbox modes must preserve the material contract/invariant the test is intended to prove. Do not mock away the boundary whose correctness is under test. When the existing harness supports it, unexpected external interactions should fail loudly rather than silently bypassing the test.

## Instrumented runtime diagnostics

When already supported by the project and relevant to the changed risk, consider instrumented runtime diagnostics for memory/resource safety, undefined/invalid runtime behavior, data races, concurrency violations, or other runtime invariants. Treat these as semantic checks; do not install a new diagnostic tool silently.

## End-to-end selection

Prioritize end-to-end tests for critical cross-layer journeys and risks. Do not duplicate every unit/component assertion at the most expensive layer merely to increase test count. E2E is most valuable when correctness depends on the assembled system or a real cross-boundary flow.

## Test data and isolation

Prefer isolated/reversible test data. Avoid production data unless explicitly authorized and safely handled. Clean up created state when appropriate and never embed secrets or sensitive personal data in fixtures/reports.
