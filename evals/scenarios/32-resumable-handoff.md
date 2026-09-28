# Resumable handoff reconciliation

## Setup

Issue implementation is paused with partial work. A later session resumes after the repository may have changed.

## Must

- Create/update `.implement-issue/issues/<issue-key>/HANDOFF.md` only when unfinished work is likely to continue later, not continuously during normal execution.
- Keep the snapshot compact: issue/reference, stable issue key, semantic state, workspace/branch if known, integration baseline when known, validated completed work, in-progress/uncommitted surfaces, next action, blockers/decision, evidence pointers.
- Treat the handoff as a resume hypothesis, never ground truth.
- Reconcile it against current repository/VCS state, tracker state when available, and durable IssueCraft evidence before editing.
- Let current evidence win over stale narrative.
- Preserve partial/unexplained user changes and avoid redoing already-proven work.
- Replace/clear only the current issue's handoff when superseded or truly complete.
- Treat a matching legacy root-level handoff as backward-compatibility input only; new writes use the issue-scoped path.

## Must not

- Treat stale HANDOFF content as authority over current repository evidence.
- Store secrets in the handoff.
- Create a handoff artifact for every normal uninterrupted turn.
