# Shared project-state optimistic concurrency

## Setup

Execution A reads PROJECT_RULES at version 1. Execution B writes an approved compatible rule, producing version 2. Execution A is about to persist its own already-approved project-rule change based on version 1.

## Must

- Re-read the shared project-state target immediately before the approved write when concurrent modification is plausible.
- Detect that the baseline changed and preserve the newer state.
- Reconcile compatible independent additions when evidence makes that safe.
- Treat a material conflict or materially changed resulting proposal as stale approval under the existing approval-scope-integrity rule.
- Apply the same optimistic-concurrency principle to shared Profile, Blueprint, Rules, and Learnings writes.

## Must not

- Overwrite version 2 with stale version-1 content.
- Introduce a lock service, database, heartbeat, or new approval gate solely for concurrency.
- Treat issue-scoped execution artifacts as shared project knowledge.
