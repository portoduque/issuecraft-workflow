# Installer adapter collision safety

## Setup

A target repository has no installed IssueCraft runtime, but already contains an `implement-issue` skill directory at one of IssueCraft's adapter destinations.

## Must

- Treat this as a first-install collision.
- Refuse before changing the target rather than silently overwriting the existing skill.
- Preserve the pre-existing adapter bytes and avoid leaving a partial IssueCraft runtime.
- Allow explicit replacement only through the documented overwrite/update path when the human intentionally chooses replacement.

## Must not

- Assume an existing same-name skill belongs to IssueCraft.
- Delete/replace the adapter during a normal first install.
- Create `.implement-issue/system/` before reporting the collision.
