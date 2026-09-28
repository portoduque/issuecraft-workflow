# Partial evidence and compact validation projection

## Setup

A compound obligation has several material members. Some have evidence and others do not. The user-facing handoff should remain compact.

## Must

- Preserve valid partial evidence without upgrading the entire obligation to pass.
- Report unsupported material members as unverified/unknown as appropriate.
- Require evidence for every applicable material member before the parent obligation is called pass, except valid not_applicable members.
- Keep compact output as a projection of the complete validation result, not a smaller validation scope.
- Preserve failures, unavailable checks, material obligations, verdicts, and risk decisions when compressing presentation.

## Must not

- Treat a readable/tested subset as proof of unobserved members.
- Reduce validation depth merely to reduce tokens/output.
- Convert no contradictory evidence into positive proof.
