# Test evidence quality over test quantity

## Setup

A change affects a documented behavior and has multiple existing test layers plus an alternate/fallback path. The full suite can pass even if the changed behavior is not asserted directly. A material acceptance criterion may also concern rendered appearance, layout, responsive behavior, or a visual state that source inspection cannot prove by itself.

## Must

- Trace each materially changed behavior or acceptance criterion to meaningful verification evidence.
- Choose the lowest-cost test layer that can faithfully prove the behavior and escalate fidelity only when lower layers cannot.
- Require assertions that would materially distinguish correct behavior from the relevant regression.
- Use rendered/runtime evidence when a material visual or layout obligation cannot be faithfully proven from source alone.
- Scope rendered checks to viewports, themes, states, platforms, and interactions supported by issue/project evidence or concrete change risk rather than inventing a universal matrix.
- Treat screenshots or other rendered artifacts as partial evidence for the surface/state actually captured, not proof of unseen states or interactions.
- Tie visual findings to an authoritative requirement/baseline or a concrete rendering defect, and reference rendered evidence when available rather than using aesthetic preference as the defect criterion.
- Treat a pre-fix reproducer as valid RED only when the targeted defect/invariant causes the failure.
- Inspect risk-relevant equivalent paths or sibling surfaces after understanding the root cause.
- Keep mocks/fakes/stubs faithful to the material contract rather than mocking away the boundary under test.
- Prioritize E2E for critical cross-layer journeys instead of duplicating all lower-level assertions.
- Use existing instrumented runtime diagnostics when supported and relevant.
- Preserve useful failure artifacts and characterize suspected flakes without rerun-until-green behavior.

## Must not

- Use overall suite pass or coverage percentage as proof that the changed behavior is tested.
- Treat source inspection or non-rendered checks as proof of a material rendered-output obligation they cannot observe.
- Invent fixed breakpoints, themes, visual states, or platform matrices without project/issue evidence.
- Turn an agent's subjective aesthetic preference into a review defect.
- Add an expensive E2E test when a cheaper faithful layer proves the same behavior.
- Accept no-throw/weak assertions that would still pass under the relevant defect.
- Count setup/environment/pre-existing failures as successful RED evidence.
