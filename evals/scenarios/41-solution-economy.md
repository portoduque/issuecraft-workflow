# Solution economy

## Setup

An issue can be solved by reusing an existing project capability, a runtime/platform primitive, an already-approved dependency, or by adding new implementation.

## Must

- Understand the affected flow and contract before optimizing the solution.
- Prefer no new implementation when the requested outcome is already satisfied truthfully.
- Search the relevant project surface for an adequate existing capability before duplicating it.
- Prefer a runtime/platform capability when evidence shows it satisfies correctness, compatibility, security, accessibility, and operational constraints.
- Prefer an already-approved dependency before adding a new dependency when it faithfully covers the need.
- Introduce new implementation only after the cheaper ownership options are insufficient.
- Judge economy by ownership and justified complexity, not raw LOC, file count, deletion count, or cleverness.

## Must not

- Treat fewer lines/files as a higher priority than correctness, security, accessibility, compatibility, reliability, or explicit requirements.
- Create speculative abstractions, wrappers, configuration, dependencies, or extension points for hypothetical future needs.
- Collapse meaningful boundaries merely to reduce file count.
