# Human Gates

The workflow should be autonomous for normal reversible engineering work and should not repeatedly pause for approval. The following gates are mandatory.

## Approval scope integrity

Human approval for a gate is scoped to the **material action or decision actually presented for review**. Approval is not a reusable token for a later operation that is materially different.

When requesting approval, describe the action/decision precisely enough for the human to understand the relevant target/environment, material scope/effects, known risk, and any precondition whose change could alter what is being authorized. Before crossing the gate, revalidate the material context needed for that action.

If the target/environment, material scope, effects, risk, or a material precondition has changed enough that the reviewed action is no longer substantively the same, treat the approval as **stale**: show the material delta and obtain fresh approval before proceeding. Do not silently recompute or expand a gated operation after approval.

Do not turn this rule into approval ceremony for ordinary reversible implementation details. Local replanning, equivalent mechanics, and other non-material execution details remain autonomous when they do not change what the human authorized.

Approval for one target, environment, operation, or risk acceptance does not imply authorization for another. A materially distinct rollback, recovery, cleanup, destructive correction, or production-impacting follow-up is evaluated under its own applicable gate rather than inheriting authorization merely because it responds to an already-approved action.

## Gate A — create/update project knowledge

Explicit human approval is required before persisting a newly inferred/proposed `PROJECT_PROFILE` or `PROJECT_BLUEPRINT`, and before changing material facts/decisions in them due to discovery or drift.

Purely mechanical metadata refreshes may be bundled with the proposed change, but must not be used to hide a material change.

## Gate B — persist new normative project rules

If the agent proposes a new rule that will govern future work, show the proposed rule and source/rationale before writing it to `PROJECT_RULES.md`.

## Gate C — destructive/production-impacting actions

Require explicit approval before an action that is materially irreversible or can affect production data/infrastructure/users when that action was not already explicitly authorized in the current request. Examples include destructive data operations, production deployment, credential rotation, or irreversible external mutations.

Do not turn ordinary file edits, local tests, dependency reads, or reversible implementation work into approval gates.

## Gate D — continuous-learning persistence and adoption

The agent may identify and draft an improvement proposal during an issue, but it must not persist that proposal, append a durable learning record, modify canonical workflow behavior, or silently add generic behavior to project rules without explicit human approval.

Persistence and adoption are distinct decisions:

1. approval to persist the proposal/learning for future reference; and
2. approval to adopt it into normative project knowledge, an adapter, or the canonical workflow.

An approved-for-record learning is not automatically approved behavior.

### Shared project-state write freshness

Before writing approved shared project state such as `PROJECT_PROFILE.yaml`, `PROJECT_BLUEPRINT.yaml`, `PROJECT_RULES.md`, or `LEARNINGS.md`, re-read the current target state when concurrent modification is plausible. If it changed since the proposal/approval baseline, reconcile rather than overwriting the newer state. Compatible independent additions may be merged when evidence makes that safe; a material conflict or materially changed proposed result makes the prior approval stale under approval-scope integrity. This is optimistic concurrency, not a lock service or new approval gate.

## Gate E — material security/performance risk acceptance

If the implementation would proceed to review with a known material security regression, an established performance-budget violation, or another explicitly identified high-impact residual engineering risk, require explicit human acceptance of that specific risk. Do not treat a generic "looks good" as risk acceptance. Prefer fixing the problem instead of requesting an exception.

## Gate F — Done

Only a human can satisfy final manual validation. The agent must not infer that manual validation passed because automated tests passed, the diff looks correct, or the agent itself exercised a UI.

Explicit confirmation such as “passed”, “approved”, “validated”, or an equivalent clear statement can authorize the `Done` transition. Ambiguous feedback does not.

## Gate G — hard-to-reverse implementation decisions

Require an explicit human decision before crossing a materially hard-to-reverse implementation boundary when the choice is not already determined by the issue, approved project knowledge, an existing public/persistence contract, or an unavoidable technical constraint.

Examples can include a new durable public contract, a persistence/data shape with expensive future migration, irreversible ownership/boundary changes, or material technology/integration lock-in.

Do not escalate ordinary local implementation choices, names, reversible refactors, or repository-conventional patterns. The gate exists for genuine one-way doors with real alternatives and meaningful reversal cost, not for routine engineering judgment.

## Gate H — material issue intent/scope drift

Require an explicit human decision when implementation evidence shows that completing the work would materially change the issue's identity rather than merely refine its execution.

Use this gate when the proposed path changes the core problem being solved, externally observable outcome, acceptance criteria, or scope boundary enough that a reasonable reviewer could consider it different work. Do not use a fixed percentage or task-count threshold.

Do **not** gate ordinary replanning, additional reversible work needed to satisfy the already-authorized intent, or implementation details that preserve the same acceptance criteria. The workflow should remain autonomous while the issue remains the same work.
