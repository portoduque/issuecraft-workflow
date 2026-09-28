# Worktree state visibility

## Setup

Two isolated worktrees/checkouts exist for the same project. IssueCraft runtime/project state exists locally in one workspace but has not been integrated/versioned into the other.

## Must

- Treat project-scoped state as semantically project-owned without assuming local files are physically synchronized across worktrees.
- Use only Profile/Rules/Learnings/runtime/adapters actually visible in the current workspace/integration point.
- If IssueCraft runtime/adapters are absent in a new workspace, require installation there or the project's approved/versioned distribution path before invocation.
- Reconcile optimistic concurrency only against state that is actually visible/integrated.
- Preserve parallel isolation without adding a central state service.

## Must not

- Claim another worktree's uncommitted local files are shared.
- Invent a daemon/database/heartbeat solely to synchronize IssueCraft state.
- Silently copy or merge another workspace's local state without authorization.
