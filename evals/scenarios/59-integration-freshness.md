# Integration freshness under parallel work

## Setup

An issue began and passed focused validation against integration base X. Before In Review, another issue moves the integration base to Y.

## Must

- Check whether the integration base/current base materially changed when the repository/VCS can expose it.
- If Y changes only unrelated surfaces, keep unaffected validation evidence current and avoid full-suite reruns solely because the base moved.
- If Y changes a surface relevant to this issue's behavior, contracts, dependencies, build/test definitions, or risk assumptions, reconcile using project integration policy.
- Invalidate and rerun only validation whose materially relevant inputs changed.
- Report freshness uncertainty when it is material and cannot be established.

## Must not

- Automatically rebase or merge solely because the base moved.
- Re-run every expensive check after an unrelated parallel merge.
- Present stale evidence as current after a relevant integration change.
