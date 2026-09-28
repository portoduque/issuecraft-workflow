# Manual Validation and the Done Gate

The canonical rules live in `../core/VALIDATION.md` and `../core/HUMAN_GATES.md`.

## Handoff

After applicable automated validation is complete, IssueCraft generates:

```text
.implement-issue/issues/<issue-key>/MANUAL_VALIDATION_PLAN.md
```

IssueCraft resolves `<issue-key>` from the strongest stable issue/reference available and reports the exact path to the human. The plan is issue-specific and derived from the issue, acceptance criteria, actual diff, affected code, project rules and automated evidence.

It can contain prerequisites/setup, happy path, edge/error cases, regression/preservation, security, performance/reliability, accessibility/compatibility, migration/recovery, observability and cleanup steps when relevant.

## Human procedure

1. Open `.implement-issue/issues/<issue-key>/MANUAL_VALIDATION_PLAN.md`.
2. Prepare the listed environment, role/permissions, test data and services.
3. Execute the numbered scenarios in order.
4. Check every expected result.
5. Execute the applicable risk-specific checks.
6. Record **PASS**, **FAIL** or **PARTIAL / NOT RUN**.
7. For **FAIL**, record the failing step plus expected and actual result.
8. Return the result to the coding agent.

## State transition

- **PASS** → Gate F is satisfied; the issue may transition from `In Review` to `Done`.
- **FAIL** → return to implementation; fix, rerun automated validation and regenerate/reconcile the manual plan.
- **PARTIAL / NOT RUN** → remain `In Review`.

Automated tests, a clean diff, agent-driven UI exercise or an inferred “looks good” never satisfy Gate F. Only a clear human validation result does.
