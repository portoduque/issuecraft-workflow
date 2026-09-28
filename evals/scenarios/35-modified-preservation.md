# Modified behavior preserves unspecified obligations

## Setup

A current contract has multiple material scenarios/fields/states. The issue modifies one of them and does not authorize removal of the others.

## Must

- Treat the modified behavior as the requested delta, not as permission to replace the whole contract arbitrarily.
- Preserve material existing clauses/scenarios/fields/states/roles/error paths not explicitly superseded.
- Add or retain proportionate regression evidence for preservation obligations.
- Detect scenario/obligation loss as a regression when a rewrite silently drops unchanged behavior.
- Mark preservation unverified when the current baseline cannot be established from evidence.

## Must not

- Claim success because the newly changed case passes while an unchanged material case disappeared.
- Infer that omission from the issue means removal authorization.
