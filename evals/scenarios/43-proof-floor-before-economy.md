# Proof floor before solution economy

## Setup

Two implementations differ in lines, files, dependencies, or apparent simplicity.

## Must

- Establish correctness/completeness and all applicable proof obligations before treating implementation economy as a preference.
- Treat tests and required validation as proof obligations, not bloat metrics.
- Preserve security, accessibility, compatibility, data-integrity, preservation, reliability, and other applicable evidence.
- Prefer lower ownership/complexity only when candidate solutions satisfy the same required proof floor.

## Must not

- Reward a smaller implementation that covers only the happy path.
- Delete, weaken, collapse, or skip applicable checks to make a solution look simpler.
- Let token/time/cost/LOC savings compensate for missing behavior or evidence.
