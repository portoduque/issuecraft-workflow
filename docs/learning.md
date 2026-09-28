# Controlled Learning

The canonical rules live in `../core/CONTINUOUS_IMPROVEMENT.md`.

IssueCraft can learn from real usage without silently self-modifying.

## Flow

```text
real evidence
  ↓
classify learning
  ↓
draft proposal
  ↓
human approval to persist
  ↓
.implement-issue/proposals/WIP-<id>.md
  ↓
optional approved record in LEARNINGS.md
  ↓
separate human approval to adopt
```

## Classes

- `generic_workflow` — plausibly useful across unrelated projects/agent hosts;
- `project_specific` — local project convention/constraint;
- `agent_adapter` — host/discovery/invocation compatibility;
- `not_actionable` — insufficient evidence or one-off.

## Important boundary

Persistence and adoption are different decisions.

A proposal or `LEARNINGS.md` entry is evidence/history only. It does not become a project rule, adapter behavior or canonical IssueCraft behavior merely because it recurred or was recorded.

Generic changes must pass the anti-bloat admission check: concrete gap/evidence, overlap review, merge-first preference, cross-project generality, ongoing cost and regression/eval proof.

Project-specific mechanical rules should prefer proportionate existing deterministic enforcement when authorized; judgement-bearing rules remain approved human-readable guidance.
