# Dependency and toolchain change evidence

## Setup

An issue changes one or more dependency/toolchain versions. A direct manifest change also alters the resolved dependency graph.

## Must

- Treat the change as behavioral and supply-chain relevant, not bookkeeping.
- Inspect the resolved dependency/lock state when the project has one.
- Review authoritative changelog/release/compatibility/deprecation/migration evidence when behavior can change.
- Consider transitive changes and their compatibility/build/release/security implications using available evidence.
- Verify the dependency's material contract through applicable project tests.
- Isolate related upgrades only as much as needed for understandable cause, evidence, review, and rollback.

## Must not

- Judge the upgrade solely from the direct manifest/version string.
- Assume semantic-version numbering proves compatibility.
- Require one dependency per change as a universal rule.
