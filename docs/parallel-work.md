# Parallel Work Safety

IssueCraft supports multiple agents/issues working on the same repository without becoming a multi-agent orchestrator.

The design is intentionally small:

1. isolate mutating work when parallel execution is intentional;
2. keep execution artifacts scoped to the issue;
3. treat shared project knowledge as optimistic-concurrency state;
4. detect relevant integration drift before `In Review`;
5. serialize only when evidence shows a real dependency/conflict.

## Workspace isolation

For intentional parallel mutation, prefer separate physical workspaces/checkouts when the environment supports them.

With Git, one practical option is a worktree per issue:

```bash
git worktree add ../my-app-issue-101 -b issue-101
git worktree add ../my-app-issue-102 -b issue-102
```

This is an example, not a canonical requirement. IssueCraft remains VCS-neutral and does not create/switch/rebase/merge/delete workspaces automatically unless explicitly authorized.

Known concurrent mutation by multiple IssueCraft executions in the same physical working tree is unsafe. Pause mutation until the work is isolated or one execution stops.

## What stays shared

Project knowledge remains shared:

```text
.implement-issue/
├── PROJECT_PROFILE.yaml
├── PROJECT_BLUEPRINT.yaml
├── PROJECT_RULES.md
├── LEARNINGS.md
└── proposals/
```

Before an approved write to shared project state, re-read the current file. If another execution changed it, reconcile instead of overwriting newer state. Compatible additions can be combined when safe; material conflicts require the applicable existing human decision.

There is no lock server, heartbeat, agent registry, or database.

## What becomes issue-scoped

Operational artifacts live under:

```text
.implement-issue/issues/<issue-key>/
├── HANDOFF.md
├── MANUAL_VALIDATION_PLAN.md
└── ISSUE_EXECUTION_REPORT.md
```

Use a stable filesystem-safe key derived from the strongest issue/reference available. If no external identifier exists, establish a local key once and reuse it for that issue.

## Collision semantics

- Different isolated workspaces + disjoint surfaces → continue in parallel.
- Different isolated workspaces + overlapping files/contracts → coordination/integration risk, not automatic blocking.
- Explicit dependency/incompatibility → respect the evidenced ordering/blocker.
- Same physical working tree + known concurrent mutation → stop mutation until isolated/serialized.
- Same issue in multiple workspaces → may be intentional alternatives or accidental duplicate work; do not assume which without evidence.

## Integration freshness

Before `In Review`, compare the issue's integration baseline/current base when the VCS exposes it.

If another issue merged only unrelated changes, keep unaffected validation evidence. If relevant code/contracts/dependencies/test definitions changed, reconcile according to project policy and rerun only the checks whose inputs became stale.

IssueCraft does not auto-rebase or auto-merge merely because the base moved.

## Legacy artifacts

Older IssueCraft versions used root-level `HANDOFF.md` and `MANUAL_VALIDATION_PLAN.md`.

A legacy artifact may be read only when its embedded issue identity unambiguously matches the current issue. New writes use the issue-scoped path. Ambiguous legacy artifacts are left untouched.
