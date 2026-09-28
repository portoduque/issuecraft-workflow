# Change coherence review

## Setup

Before In Review, the issue, project contracts, implementation diff, tests, and manual validation artifact are all available.

## Must

- Reconcile issue intent/acceptance, project/repository contracts, behavior delta when applicable, implementation diff, automated evidence, and manual validation as one change.
- Detect contradictions in any direction, including unauthorized behavior, missing required behavior, tests proving the wrong outcome, preservation loss, or a manual plan that misses a material changed risk.
- Require justification traceability for every material diff change to a legitimate requirement/invariant/risk/compatibility/enabling need.
- Make findings evidence-backed and include a concrete corrective action when known.
- Allow a clean review to produce zero findings.

## Must not

- Treat an old plan as authoritative after current evidence disproves it.
- Invent findings merely to make review look productive.
- Treat unrelated cleanup as automatically in scope.
