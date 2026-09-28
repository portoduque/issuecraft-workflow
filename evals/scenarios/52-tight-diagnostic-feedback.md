# Tight diagnostic feedback loop

## Setup

A difficult bug is intermittent, environment-dependent, or performance-related. A faithful unit/integration RED test may not be immediately available, but traces, measurements, replayable artifacts, targeted commands, or scoped instrumentation can provide a discriminating signal.

## Must

- Establish the tightest feasible feedback signal for the user's actual symptom before entering repeated speculative fix attempts.
- Prefer a signal that is specific, fast, repeatable/high-reproduction, and agent-runnable when feasible.
- Tighten or minimize the signal when doing so reduces the hypothesis space without changing the symptom.
- Use the strongest available evidence when a faithful local automated RED test is not practical.
- Trigger diagnostic reset after repeated failed fixes without materially new evidence.
- After the fix, rerun the original symptom-specific signal/reproducer when feasible.

## Must not

- Require universal TDD or a local failing test as a prerequisite for every bug fix.
- Treat an unrelated setup/environment failure as proof of the target defect.
- Keep patching after repeated failures without changing the evidence/hypothesis.
- Replace production/runtime/performance evidence with a shallow test that cannot reproduce the actual failure.
