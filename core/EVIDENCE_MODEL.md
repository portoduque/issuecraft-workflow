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
