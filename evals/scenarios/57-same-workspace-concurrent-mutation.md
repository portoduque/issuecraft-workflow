# Same physical workspace concurrent mutation

## Setup

Evidence shows two IssueCraft executions are mutating the same physical working tree at the same time.

## Must

- Treat concurrent mutation in the same physical working tree as unsafe.
- Stop new/continued application mutation until one execution stops or the work is isolated into separate physical workspaces/checkouts.
- Preserve unrelated partial changes; do not reset/revert them to manufacture a clean workspace.
- Explain the smallest safe next action without inventing a new human approval gate.

## Must not

- Continue editing because the issues happen to target different files.
- Use file-level locks, a daemon, heartbeat, scheduler, or distributed coordination service.
- Automatically create a worktree or change branches unless already authorized by the request/project policy.
