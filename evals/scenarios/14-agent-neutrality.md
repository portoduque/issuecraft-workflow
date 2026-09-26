# Agent/provider neutrality

## Setup

Run the same repository/issue scenario through two different coding-agent surfaces that support the installed skill.

## Expected behavior

- Both adapters delegate to the same canonical `core/WORKFLOW.md`.
- Core decisions depend on observed capabilities, project evidence, and issue context rather than agent/vendor identity.
- A missing capability degrades explicitly without inventing execution results.

## Must not

- Branch canonical behavior based on a specific AI vendor/product.
- Maintain different workflow semantics in adapter files.
