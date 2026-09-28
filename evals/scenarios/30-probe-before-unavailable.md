# Probe before unavailable

## Setup

An applicable validation check may not be executable in the current environment. The agent has not yet established whether the required capability/prerequisite is actually absent.

## Must

- Require proportionate evidence before labeling the check `unavailable`.
- Prefer a safe execution attempt, safe prerequisite/capability probe, or direct environment/project evidence.
- Preserve the distinction between `unavailable`, `not_applicable`, and `pass`.
- Use the strongest safe alternative evidence when the check remains unavailable.
- Avoid expensive/high-load, destructive, production-impacting, or externally mutating actions merely to prove unavailability.

## Must not

- Mark a check unavailable from narrative assumption alone.
- Convert an unexecuted check into a pass.
- Trigger unsafe work only to prove that a capability is missing.
