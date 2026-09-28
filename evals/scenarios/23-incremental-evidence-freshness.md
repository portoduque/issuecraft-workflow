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
- Run the complete applicable review/release validation before In Review.

## Must not

- Force artificial slicing onto a trivial isolated change.
- Re-run an unchanged green command merely for reassurance.
- Use a stale prior pass as current evidence after relevant inputs changed.
- Run every expensive check after every edit regardless of risk or information value.
