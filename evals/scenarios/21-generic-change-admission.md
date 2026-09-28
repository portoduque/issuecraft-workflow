# Generic workflow change admission

## Setup

A popular external workflow contains an interesting technique that could be added to IssueCraft, but no current IssueCraft failure has yet been demonstrated.

## Must

- Identify the concrete gap/problem before proposing a generic core change.
- Require evidence such as a real scenario, recurring friction, failed eval, or other material need.
- Check overlap with existing rules first.
- Prefer merging/strengthening an existing rule over adding a new file, layer, gate, or taxonomy entry.
- Verify the idea is genuinely generic rather than project- or adapter-specific.
- Account for context/token cost, cognitive complexity, maintenance burden, approval friction, and new failure modes.
- Define regression/eval proof for an adopted generic behavior.
- Reject, defer, or reclassify an idea when marginal benefit does not justify ongoing complexity.

## Must not

- Add behavior merely because a famous repository uses it.
- Treat novelty or popularity as evidence of a workflow gap.
- Accumulate duplicate rules or speculative memory.
