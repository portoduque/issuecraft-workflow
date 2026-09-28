# Contributing to IssueCraft Workflow

Contributions are welcome. The main architectural constraint is that the canonical core remains provider-, stack-, framework-, language-, database-, test-tool-, CI-, and tracker-neutral.

## Before changing behavior

1. Describe the problem with a concrete scenario, recurring friction, or failed eval.
2. Decide whether the change is generic, project-specific, adapter-specific, or not actionable.
3. Check whether an existing canonical rule already covers the need.
4. Prefer strengthening/simplifying an existing rule over adding another file, layer, gate, taxonomy item, or duplicated instruction.
5. Confirm a generic change remains useful across unrelated projects/agent hosts and justify its context/token, cognitive, maintenance, and approval cost.
6. Keep project-specific conventions out of `core/`.
7. Add or update a deterministic contract eval for adopted generic behavioral changes.
8. Add repository tests when the invariant can be verified deterministically.
9. Add/update a live-agent fixture scenario when behavior can only be validated by observing an actual agent across repository changes or multiple turns.

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
- behavior-to-evidence test traceability, evidence-or-zero for material obligations, compound-obligation decomposition, meaningful assertions, lowest sufficient test fidelity, and evidence-backed diff review;
- diagnostic reset instead of repeated speculative fixes without new evidence;
- progressive issue-context retrieval and risk-based impact reconnaissance without exhaustive repository reading;
- version-aware authoritative-source verification when correctness depends on external/version-sensitive behavior;
- thin verifiable increments, risk-first slices, and evidence freshness for non-trivial work;
- quality-bar integrity review, compatibility-safe migrations/cutovers, dependency lock-state evidence, approved-baseline ratchets, and probe-before-unavailable evidence;
- risk-based isolated discrimination/fault checks when test effectiveness is materially uncertain;
- resumable handoff snapshots that are reconciled against current repository/VCS/tracker evidence before edits;
- human gating for genuine hard-to-reverse one-way-door choices without turning ordinary reversible engineering into approval ceremony;
- anti-bloat admission for generic workflow growth, including procedure portability instead of implementation-specific workarounds;
- compact user-facing handoffs without loss of material evidence, failures, unavailable checks, risks, or human gates;
- human ownership of persistent learning, material risk acceptance, and final `Done`; recurrence may strengthen evidence but never auto-adopt behavior;
- installer protection against managed symlink redirection;
- release archives free from VCS metadata and local caches;
- immutable-SHA pinning for GitHub Actions dependencies.

## Validator resistance

When changing a deterministic validator or its contract, add/update a resistance test that mutates a known-good fixture/repository copy and proves the validator rejects the broken invariant. Include a negative control where practical so the validator is also proven not to reject harmless changes.
