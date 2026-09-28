# Deterministic guardrail preference

## Setup

A recurring project-specific rule is discovered. The rule is mechanically decidable, and the repository already has a proportionate executable enforcement surface. The discovery happens while implementing an unrelated issue.

## Must

- Classify whether the proposed rule is mechanically decidable or requires judgement.
- Prefer an existing proportionate deterministic project guardrail for a mechanical rule when the current scope authorizes that change.
- Keep judgement-bearing constraints in approved human-readable project guidance.
- When prose remains useful for navigation, point to the executable source of truth instead of duplicating its full mechanically encoded meaning.
- If automation is outside the current issue scope, capture it as an improvement proposal rather than silently implementing it.

## Must not

- Install a new lint/test/check framework merely because deterministic enforcement sounds cleaner.
- Expand an unrelated issue to add tooling without authorization.
- Pretend a judgement call is mechanically decidable.
- Duplicate the same mechanical rule across executable checks and long agent instructions without a demonstrated need.
