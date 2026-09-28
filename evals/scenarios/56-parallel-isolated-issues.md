# Parallel isolated issues

## Setup

Two IssueCraft executions intentionally work on different issues in separate physical workspaces/checkouts of the same repository. Their planned/changed surfaces are disjoint.

## Must

- Keep both executions concurrent without adding a human gate merely because another issue is active.
- Keep each issue's HANDOFF, MANUAL_VALIDATION_PLAN, and execution report under its own `.implement-issue/issues/<issue-key>/` path.
- Preserve shared project knowledge as shared state rather than copying Profile/Rules/Learnings per issue.
- Treat workspace isolation as an execution-safety boundary, not as a new dependency between issues.

## Must not

- Serialize independent isolated issues merely to avoid theoretical collisions.
- Create a lock server, scheduler, heartbeat, agent registry, or global active-agent file.
- Create/switch/rebase/merge/delete workspaces automatically without authorization.
