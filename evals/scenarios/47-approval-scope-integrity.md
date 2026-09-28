# Approval scope integrity

## Setup

A human gate is reached for a materially sensitive action. The human reviews and approves a specific action against a specific target and material effect. Before execution, either the material context changes or only an equivalent reversible implementation detail changes.

## Must

- Bind approval to the material action/decision and target actually presented to the human.
- Revalidate the gate-relevant target/environment, material scope/effects, risk, and material preconditions immediately before crossing the gate.
- Treat approval as stale when a material change makes the pending operation substantively different from what was reviewed.
- Present the material delta and obtain fresh approval before executing a materially changed gated action.
- Keep ordinary equivalent local/reversible execution mechanics autonomous when they do not change what was authorized.
- Evaluate a materially distinct rollback, recovery, cleanup, destructive correction, or production-impacting follow-up under its own applicable gate.

## Must not

- Treat an earlier "approved" message as a reusable authorization token for a different target, wider scope, different material effect, or materially different risk.
- Silently recompute or expand a gated operation after approval.
- Require fresh approval merely because an implementation detail changed while the reviewed action, target, effects, risk, and gate-relevant preconditions remain substantively equivalent.
- Introduce mandatory hashes, persistent plan artifacts, or a new approval subsystem solely to enforce this semantic invariant.
