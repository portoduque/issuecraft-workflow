# Human Gates

The workflow should be autonomous for normal reversible engineering work and should not repeatedly pause for approval. The following gates are mandatory.

## Gate A — create/update project knowledge

Explicit human approval is required before persisting a newly inferred/proposed `PROJECT_PROFILE` or `PROJECT_BLUEPRINT`, and before changing material facts/decisions in them due to discovery or drift.

Purely mechanical metadata refreshes may be bundled with the proposed change, but must not be used to hide a material change.

## Gate B — persist new normative project rules

If the agent proposes a new rule that will govern future work (for example an architectural prohibition, testing policy, migration policy, or status mapping), show the proposed rule and source/rationale before writing it to `PROJECT_RULES.md`.

## Gate C — destructive/production-impacting actions

Require explicit approval before an action that is materially irreversible or can affect production data/infrastructure/users when that action was not already explicitly authorized in the current request. Examples include destructive data operations, production deployment, credential rotation, or irreversible external mutations.

Do not turn ordinary file edits, local tests, dependency reads, or reversible implementation work into approval gates.

## Gate D — workflow improvement adoption

The agent may generate an improvement proposal, but may not modify the canonical workflow or silently add generic behavior to project rules without human approval.

## Gate E — material security/performance risk acceptance

If the implementation would proceed to review with a known material security regression, an established performance-budget violation, or another explicitly identified high-impact residual engineering risk, require explicit human acceptance of that specific risk. Do not treat a generic "looks good" as risk acceptance. Prefer fixing the problem instead of requesting an exception.

## Gate F — Done

Only a human can satisfy final manual validation. The agent must not infer that manual validation passed because automated tests passed, the diff looks correct, or the agent itself exercised a UI.

Explicit confirmation such as “passed”, “approved”, “validated”, or an equivalent clear statement can authorize the `Done` transition. Ambiguous feedback does not.
