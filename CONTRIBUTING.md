# Contributing

Contributions are welcome. The main constraint is architectural: **the canonical core must remain provider-, stack-, framework-, language-, database-, test-tool-, CI-, and tracker-neutral.**

## Before changing behavior

1. Describe the problem with a concrete scenario or failed eval.
2. Decide whether the change is generic or project-specific. Project-specific conventions do not belong in `core/`.
3. Prefer changing one canonical rule over adding provider-specific branches.
4. Add/update an eval scenario.
5. Run:

```bash
python scripts/validate_repo.py
python -m unittest discover tests -v
```

## Compatibility adapters

Adapters may mention a specific product only when necessary for discovery/invocation. They must delegate behavior to the canonical core rather than reimplement it.

## Changes to human gates

Human-approval rules are security and governance boundaries. Changes to them should be explicit in the PR description and include a regression scenario.

## Quality invariants

Changes that affect the canonical workflow must preserve:

- provider/agent neutrality in `core/`;
- stack/framework/language neutrality in `core/`;
- mandatory security-impact and performance-impact triage;
- comprehensive risk-based test selection with `pass/fail/unavailable/not_applicable` semantics;
- human ownership of material risk acceptance and final `Done`;
- installer protection against writing through managed symlinks.

Add or update an eval scenario for generic behavioral changes.
