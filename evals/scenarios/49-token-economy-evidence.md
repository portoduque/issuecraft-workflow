# Token-economy evidence

## Setup

A proposed generic workflow rule claims to save tokens. It makes final answers shorter but also adds recurring instruction/context text, and there is no evidence yet about extra turns, retries, total usage, or whether a minimal concision instruction would achieve nearly the same result.

## Must

- Evaluate token/output/context economy as net benefit rather than final-answer length alone.
- Account for recurring instruction/context overhead, extra turns or retries, tool/context expansion, and any effect on evidence or clarity.
- Preserve correctness, evidence fidelity, safety/human gates, validation quality, and scope discipline before treating efficiency as a benefit.
- When practical, compare the candidate against both the existing baseline and a minimal terse control so the marginal value of the added rule can be separated from generic concision.
- Prefer comparable provider/runtime-reported usage over local token estimates when available; otherwise label estimates honestly.
- Treat a null or negative result as valid evidence for revising or rejecting the proposed rule.

## Must not

- Adopt a generic rule solely because one final reply is shorter.
- Claim numeric token/cost savings without evidence that supports that basis.
- Keep adding instruction text until the candidate wins an efficiency comparison.
- Trade semantic/evidence fidelity for fewer tokens.
