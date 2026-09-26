# Stack/language neutrality

## Setup

Evaluate two unrelated repositories with different languages, runtimes, dependency managers, persistence systems, test frameworks, and build tools.

## Expected behavior

- Discovery infers each repository only from evidence.
- The canonical workflow uses semantic concepts such as build, test, migration, security and performance rather than hardcoded technology commands.
- Unknown tools remain unknown until supported by evidence.
- Project-specific rules remain local and do not leak into canonical core.

## Must not

- Prefer a language/framework/database/package manager because it is common or familiar.
- Hardcode commands from the other repository.
