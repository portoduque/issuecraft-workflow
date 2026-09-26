# Example — Drift

Approved Profile records one dependency manager. Later evidence shows the old lockfile disappeared, a different lockfile appeared, and the manifest explicitly names the new manager.

Expected behavior:

1. Cheap drift preflight detects conflicting evidence.
2. Report `before`, `observed`, evidence, and current-issue impact.
3. Do not edit the Profile automatically.
4. Ask for approval of the proposed Profile change if it matters.
5. Continue only when the issue can be implemented safely under the resolved/current context.
