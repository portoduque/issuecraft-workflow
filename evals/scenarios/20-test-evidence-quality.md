# Test evidence quality over test quantity

## Setup

A change affects a documented behavior and has multiple existing test layers plus an alternate/fallback path. The full suite can pass even if the changed behavior is not asserted directly.

## Must

- Trace each materially changed behavior or acceptance criterion to meaningful verification evidence.
- Choose the lowest-cost test layer that can faithfully prove the behavior and escalate fidelity only when lower layers cannot.
- Require assertions that would materially distinguish correct behavior from the relevant regression.
- Treat a pre-fix reproducer as valid RED only when the targeted defect/invariant causes the failure.
- Inspect risk-relevant equivalent paths or sibling surfaces after understanding the root cause.
- Keep mocks/fakes/stubs faithful to the material contract rather than mocking away the boundary under test.
- Prioritize E2E for critical cross-layer journeys instead of duplicating all lower-level assertions.
- Use existing instrumented runtime diagnostics when supported and relevant.
- Preserve useful failure artifacts and characterize suspected flakes without rerun-until-green behavior.

## Must not

- Use overall suite pass or coverage percentage as proof that the changed behavior is tested.
- Add an expensive E2E test when a cheaper faithful layer proves the same behavior.
- Accept no-throw/weak assertions that would still pass under the relevant defect.
- Count setup/environment/pre-existing failures as successful RED evidence.
