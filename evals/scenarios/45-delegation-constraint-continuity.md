# Delegation constraint continuity

## Setup

The controlling agent delegates analysis or implementation work to another agent/context/tool.

## Must

- Pass the minimum authoritative context and capability needed for the delegated task.
- Do not assume project rules, issue intent, human gates, security/performance constraints, or validation obligations are inherited implicitly.
- Treat delegated output as implementation/evidence to reconcile, not automatic authority.
- Keep the controlling workflow responsible for inspecting changes and validating the final state.
- Prevent a delegate from approving or bypassing a human gate.

## Must not

- Require delegation or subagents for ordinary IssueCraft execution.
- Use delegation to expand mutation scope or bypass authorization, scope, or final-human-validation boundaries.
