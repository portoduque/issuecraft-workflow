# Contributing to IssueCraft Workflow

Contributions are welcome. The main architectural constraint is that the canonical core remains provider-, stack-, framework-, language-, database-, test-tool-, CI-, and tracker-neutral.

## Before changing behavior

1. Describe the problem with a concrete scenario or failed eval.
2. Decide whether the change is generic, project-specific, or adapter-specific.
3. Keep project-specific conventions out of `core/`.
4. Prefer changing one canonical rule over adding provider-specific branches.
5. Add or update a deterministic contract eval for generic behavioral changes.
6. Add repository tests when the behavior can be verified deterministically.
7. Add/update a live-agent fixture scenario when the behavior can only be validated by observing an actual agent across repository changes or multiple turns.

Run:

```bash
python scripts/validate_repo.py
python scripts/run_evals.py
python scripts/run_live_evals.py validate
python -m unittest discover tests -v
```

## Compatibility adapters

Adapters may mention a specific product only when necessary for discovery/invocation. They must delegate behavior to the canonical core rather than reimplement it.

## Changes to human gates

Human-approval rules are security and governance boundaries. Changes to them must be explicit in the PR description and include regression coverage.

## Quality invariants

Changes that affect the canonical workflow must preserve:

- provider/agent neutrality in `core/`;
- stack/framework/language neutrality in `core/`;
- mandatory security-impact and performance-impact triage;
- comprehensive risk-based test selection with `pass/fail/unavailable/not_applicable` semantics;
- human ownership of persistent learning, material risk acceptance, and final `Done`;
- installer protection against managed symlink redirection;
- release archives free from VCS metadata and local caches;
- immutable-SHA pinning for GitHub Actions dependencies.
