# Evidence Model

Project knowledge must be traceable to evidence.

## Evidence sources

Use explicit source types such as:

- `manifest` — dependency/project manifests.
- `lockfile` — resolved dependency/package manager evidence.
- `config` — tool/framework/build configuration.
- `source` — imports, entrypoints, annotations, APIs, file extensions, generated headers.
- `script` — scripts/Makefiles/task runners.
- `ci` — pipeline definitions.
- `migration` — migration files/config/history.
- `runtime` — successful command output or introspection.
- `documentation` — repository documentation/specification.
- `human` — explicit human decision/statement.

## Confidence

- **high:** direct, unambiguous evidence or multiple corroborating sources.
- **medium:** credible but indirect evidence, or documentation not yet corroborated by implementation.
- **low:** weak/ambiguous signal worth surfacing but not safe to treat as established.

Confidence never upgrades an inference into a fact. Record the underlying evidence.

## Unknown vs not detected vs absent

- `unknown`: insufficient evidence or not reliably determined.
- `not_detected`: the workflow searched relevant evidence locations and found no positive signal. This does **not** prove nonexistence.
- `absent`: use only when absence itself is directly established by a reliable source/constraint; use sparingly.
- `not_applicable`: the concept does not apply by an approved or clearly established project fact.

## Conflicts

When evidence conflicts:

1. Preserve both signals.
2. Prefer direct current repository/runtime evidence over stale narrative documentation for the Profile, but do not silently rewrite the documented intent.
3. Lower confidence or mark the fact `conflict`.
4. Surface material conflicts before they drive implementation.

## Partial evidence

Partial evidence supports only the conclusion it actually proves.

- Evidence for some members of a compound obligation does not prove the unobserved members.
- Evidence from one path, role, environment, mode, or scenario does not automatically generalize to another materially distinct one.
- Continue using valid partial evidence, but mark the unsupported remainder unverified/unknown as appropriate.
- Do not convert "no contradictory evidence found" into positive proof.
- A bounded, paginated, truncated, sampled, or partially readable result remains partial evidence. An item missing from the returned subset is not evidence that it is absent from the complete set.

## Derived/indexed evidence integrity

Indexes, dependency/knowledge graphs, semantic engines, caches, generated summaries, static-analysis projections, and similar derived views can be high-signal evidence, but they remain projections of an underlying subject.

Before using derived evidence to support a decision, completeness claim, or absence claim, consider the properties that materially affect that claim:

- **subject freshness** — whether the view describes the current relevant code/configuration/revision/state;
- **applicability** — whether the result actually fits the decision's subject, scope, version/environment, mode/platform, and relevant contract rather than merely resembling it;
- **coverage** — whether the relevant files, languages, relation types, paths, modes, or environments are actually represented;
- **completeness limits** — pagination, result caps, depth limits, sampling, truncation, or omitted regions;
- **degraded/partial state** — parse failures, stale caches, unavailable dependencies, timeouts, or other conditions that reduce fidelity;
- **known blind spots** — dynamic behavior, reflection, generated code, framework conventions, external systems, or other relationships the mechanism cannot reliably observe;
- **provenance** — whether a relation/result is directly observed/extracted or inferred/heuristic.

A high-ranked, nearest, or otherwise retrieved recommendation is not automatically a project fact. When applicability is material and uncertain, narrow or reframe retrieval, corroborate with stronger project/runtime evidence, or keep the conclusion explicitly unverified/fallback rather than persisting it as authoritative knowledge.

A zero/empty derived result supports `absent` only when currentness, applicability, relevant coverage, completeness, and mechanism limits make that conclusion reliable. Otherwise classify it as `not_detected` or `unknown` as appropriate and use stronger evidence when the distinction is material.

When current authoritative repository/runtime evidence conflicts with a derived view, prefer the authoritative evidence for the immediate decision and preserve the material discrepancy rather than silently treating the derived view as current truth.

## Evaluation evidence independence

When an evaluation oracle, reference answer, benchmark ground truth, or expected ordering is derived wholly or partly from the same mechanism being evaluated, disclose that circularity. Treat the result as consistency/upper-bound evidence rather than independent proof of correctness, and seek an independent signal when the adoption claim depends on correctness of that mechanism.

## Mutable evidence and conversation memory

Conversation memory, a prior plan, or an earlier handoff can point to evidence but is not a substitute for the current authoritative source when that source is mutable. At resume and material phase transitions, re-read the specific live issue/project/rule/configuration/code/validation inputs on which the next decision depends.

## No invented commands

A command belongs in the Profile only when supported by a manifest/script/docs/CI/runtime evidence. Do not transform a generic convention into a project fact.

## Evidence detail

Record enough detail to re-check later without copying secrets. Prefer a file path plus the relevant key/section rather than sensitive values. Example:

```yaml
evidence:
  - type: manifest
    path: package.json
    detail: packageManager field
```

Never store credential values, connection secrets, tokens, or private keys in project context.
