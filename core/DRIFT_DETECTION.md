# Drift Detection

Drift detection prevents a once-correct Profile from becoming stale without forcing a full rediscovery on every issue.

## Cheap preflight

When an approved Profile exists, re-check the evidence most likely to change engineering behavior:

- project/workspace manifests;
- lockfiles/dependency manager markers;
- language/runtime/toolchain version markers;
- framework/build configuration;
- test/lint/format/typecheck configuration and scripts;
- security tooling, policies, trust-boundary documentation, and security gates recorded in the Profile;
- performance tooling, budgets, baselines, capacity/SLO evidence, and performance gates recorded in the Profile;
- observability/health configuration that materially affects validation;
- database/data-access and migration configuration;
- CI/CD definitions;
- major component/module structure;
- commands recorded in the Profile;
- relevant architecture/rules files.

Use the Profile's own evidence paths first, then inspect newly appeared competing signals.

## Material drift

Treat a change as material when it can alter how issues should be implemented or validated, for example:

- dependency/package manager changed;
- language/runtime/framework added/replaced/removed;
- database or migration mechanism changed;
- test/build/lint/typecheck command changed;
- security mechanism/policy/gate materially changed;
- performance budget/baseline/tooling materially changed;
- observability or health verification materially changed;
- CI/release strategy materially changed;
- monorepo/service boundaries changed;
- previously recorded evidence disappeared or conflicts with new evidence.

## Response

1. Record `before`, `observed`, and evidence.
2. Do not edit the Profile automatically.
3. Determine whether the current issue can proceed safely without resolving the drift.
4. If drift affects the current plan, present it before implementation.
5. Propose the minimal Profile update and request approval.
6. After approval, update evidence/confidence and `last_verified` metadata.

## Blueprint divergence

If observed reality conflicts with an approved Blueprint, label it separately as `blueprint_divergence`. Ask whether the intended architecture changed or the implementation needs correction. Never rewrite both documents to match automatically.
