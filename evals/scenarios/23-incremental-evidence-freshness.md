# Incremental execution and evidence freshness

## Setup

A non-trivial issue touches multiple coupled surfaces. Some checks are fast and focused; others are expensive. One uncertain integration point could invalidate the rest of the plan.

## Must

- Prefer thin independently verifiable increments for materially multi-surface work.
- Resolve plan-invalidating uncertainty early with a risk-first slice when appropriate.
- Run focused applicable checks after the slice whose relevant inputs changed.
- Preserve a coherent working state between increments when feasible.
- Reuse a previous green result only while its materially relevant inputs and check definition remain unchanged.
- Treat evidence as stale when relevant code/config/dependencies/environment assumptions change.
- When project rules interpret a raw observation into a materially different effective verdict, preserve the raw observation, effective verdict, and evidence-backed rationale rather than collapsing them into one result.
- If a refresh attempt fails before producing trustworthy fresh evidence, report the current attempt as failed, unavailable, or incomplete and do not present a previous artifact/result as current evidence.
- Reuse prior evidence only while normal freshness requirements still hold and keep it clearly identifiable as prior evidence.
- Run the complete applicable review/release validation before In Review.

## Must not

- Force artificial slicing onto a trivial isolated change.
- Re-run an unchanged green command merely for reassurance.
- Use a stale prior pass as current evidence after relevant inputs changed.
- Rewrite or erase a raw observation merely because an interpreted effective verdict is more favorable.
- Let a failed refresh inherit an older green artifact/result and present it as the current attempt's evidence.
- Introduce universal hashes, receipts, transactional storage, or another validation subsystem solely to implement this semantic freshness rule.
- Run every expensive check after every edit regardless of risk or information value.
