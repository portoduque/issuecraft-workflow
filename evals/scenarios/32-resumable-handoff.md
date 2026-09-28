# Resumable handoff reconciliation

## Setup

Issue implementation is paused with partial work. A later session resumes after the repository may have changed.

## Must

- Create/update `.implement-issue/HANDOFF.md` only when unfinished work is likely to continue later, not continuously during normal execution.
- Keep the snapshot compact: issue/reference, semantic state, workspace/branch if known, validated completed work, in-progress/uncommitted surfaces, next action, blockers/decision, evidence pointers.
- Treat the handoff as a resume hypothesis, never ground truth.
- Reconcile it against current repository/VCS state, tracker state when available, and durable IssueCraft evidence before editing.
- Let current evidence win over stale narrative.
- Preserve partial/unexplained user changes and avoid redoing already-proven work.
- Replace/clear the handoff when superseded or truly complete.

## Must not

- Treat stale HANDOFF content as authority over current repository evidence.
- Store secrets in the handoff.
- Create a handoff artifact for every normal uninterrupted turn.
