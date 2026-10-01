# Manual Validation Plan

## Issue

- Identifier:
- Issue key:
- Title:

## Validation subject

Record the strongest practical identity of the implementation state this plan validates. Do not invent a hash when the project/runtime does not already provide one usefully.

- Repository/workspace:
- Branch/reference:
- Revision / integration base when available:
- Working-tree/material changed-state note:
- Other subject identity/evidence:

If the materially relevant implementation changes after this subject is captured, reconcile this plan and affected automated evidence before treating a prior human PASS as current.

## Objective

State exactly what this validation proves.

## Prerequisites

-

## Setup

1.

## Scenario 1 — primary behavior

1. Action:
   - Expected:
2. Action:
   - Expected:

## Edge / error scenarios

### Scenario

1.
   - Expected:

## Regression / preservation checks

- [ ] Confirm nearby behavior most exposed by the diff still works.
- [ ] Confirm material behavior on a modified surface that was not explicitly removed remains preserved.

## Security-sensitive checks (when applicable)

- [ ] Authorization/isolation/trust-boundary behavior remains correct.
- [ ] Sensitive data/secrets are not exposed in UI, output, logs, or errors.

## Performance/reliability checks (when applicable)

- [ ] Representative behavior remains within known project budgets/baselines.
- [ ] No obvious resource, concurrency, or responsiveness regression is observed.

## Accessibility / compatibility / migration / recovery checks (when applicable)

- [ ]

## Cleanup

1.

## Human result

- [ ] PASS
- [ ] FAIL
- [ ] PARTIAL / NOT RUN

If FAIL, record failing step, expected result, actual result, and any useful environment details.

A PASS applies only to the validation subject above (or a materially equivalent current state). If the implementation changed materially after validation, mark the prior PASS stale and validate the reconciled current subject before `Done`.
