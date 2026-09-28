# Issue Lifecycle

The workflow uses semantic states so it can operate with any tracker or with no tracker.

## Canonical states

```text
Todo → In Progress → In Review → Done
            ↑             │
            └── human validation failed
```

A tracker may use different names. Map by meaning, not by string similarity alone. Do not create/change tracker workflow states unless explicitly authorized.

## Issue resolution

Use the strongest available source and preserve traceability. If tracker access exists, read the live issue. Otherwise use user-supplied text/specs.

Do not invent missing acceptance criteria. You may derive an implementation interpretation from the described outcome, but label it as an interpretation and avoid expanding scope.

Treat the issue's **intent and scope identity** as distinct from the implementation plan. If evidence only changes how the same accepted outcome should be implemented, replan autonomously. If the core problem, externally observable outcome, acceptance criteria, or material scope boundary would change, use the material issue intent/scope drift human gate before proceeding.

When repository/tracker evidence reveals another active change on the same high-collision contract/surface, report the coordination risk. Do not infer a dependency or execution order unless it is explicitly documented or otherwise evidenced.

## State transitions

### → In Progress

Transition when project onboarding/drift checks are resolved enough to start implementation and the agent is actually beginning work.

### → In Review

Transition only after:

- the intended implementation is complete without silently narrowing/deferring required behavior;
- behavior-delta/preservation obligations are reconciled when applicable;
- applicable automated validation has run or any unavailable checks are explicitly documented;
- change coherence review finds no unresolved release-blocking contradiction;
- the issue-specific manual validation plan has been generated.

### → Done

Transition only after explicit human confirmation that manual validation passed.

### In Review → In Progress

If human validation fails, capture the observed failure, reopen implementation, repair it, rerun relevant automated checks, and return with an updated manual plan.

## No tracker-write capability

Never claim a transition occurred. Report: `Requested semantic transition: <state>; tracker write unavailable.` Continue implementation when the missing state write does not block technical work.

## Ambiguous tracker mapping

If multiple tracker states plausibly match a canonical state and writing the wrong one matters, ask once for mapping/approval and persist the approved mapping as a project rule only with approval.
