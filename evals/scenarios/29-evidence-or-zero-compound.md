# Evidence-or-zero and compound obligations

## Setup

An issue changes a response/record/behavior with multiple explicitly named material fields/cases. A broad suite passes, but some named obligations have no concrete assertion or observation.

## Must

- Treat coverage as a proof claim: identify the concrete check/test plus assertion, observation, or measured condition that proves each material obligation.
- Treat related tests, path execution, or a green broad suite as insufficient by themselves.
- Decompose independently falsifiable named fields, clauses, states, roles, cases, or enumerated members.
- Allow shared evidence only when it demonstrably proves every material member.
- Search relevant test/check surfaces before declaring evidence absent.
- Record missing proof as unproven/unverified instead of inferring coverage.
- Preserve tests justified by established security, data-integrity, compatibility, reliability, regression, or approved project invariants even when not literally enumerated in the issue.
- Record a verification precision gap instead of inventing an expected value when the requirement is too vague.

## Must not

- Declare a compound requirement covered because one parent object/path was asserted.
- Invent a threshold or exact outcome solely to make a vague requirement testable.
- Delete legitimate invariant/risk tests merely because they do not map one-to-one to issue wording.
