# Comprehensive risk-based test selection

## Setup

A change affects business logic, a persistence boundary, an external contract, accessibility-visible UI, and a concurrency-sensitive operation. Existing repository infrastructure includes several different test mechanisms.

## Expected behavior

- Consider the complete semantic test taxonomy in `TEST_STRATEGY.md`.
- Select applicable types across functional, regression, negative/boundary, integration/contract, concurrency, accessibility, security and performance/reliability families.
- Mark irrelevant types `not_applicable` with rationale and applicable-but-unrunnable types `unavailable`.
- Reuse project test mechanisms and commands from evidence.
- For a reproduced bug, prefer a durable regression test when feasible.

## Must not

- Reduce validation to a single generic `test` command when multiple risk-relevant suites exist.
- Run every possible test type indiscriminately when it is unrelated to the change.
- Treat `unavailable` as `pass`.
