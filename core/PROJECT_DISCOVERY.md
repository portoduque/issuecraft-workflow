# Project Discovery

Use this phase when meaningful implementation/configuration evidence exists and no approved `PROJECT_PROFILE` is available, or when a full rediscovery is required.

## Goal

Produce an evidence-backed proposal describing **what the repository currently is**, without forcing it into a predetermined stack taxonomy.

## Ignore workflow/runtime files

Exclude `.implement-issue/system/`, the `implement-issue` skill adapters, VCS internals, dependency caches, generated build outputs, and vendored dependencies from stack inference unless the target project intentionally owns such files.

## Discovery passes

### Pass A — repository shape

Inspect root and meaningful subprojects/modules. Identify whether the repository is single-project, monorepo, multi-service, library collection, infrastructure repository, or mixed. Do not assume one global stack when components differ.

### Pass B — manifests and dependency management

Find project manifests, dependency declarations, lockfiles, workspace files, task runners, toolchain/version files, containers, and environment templates. Infer package/dependency managers only from evidence.

### Pass C — languages, runtimes, frameworks

Use file types, manifests, imports, entrypoints, configuration, runtime files, generated metadata, and documentation. Record multiple languages/frameworks when applicable and scope them to components.

### Pass D — persistence and migrations

Look for database drivers, ORM/data-access configuration, schema definitions, migration directories/tools, local containers, seed/fixture systems, and documented data stores. Do not store secrets.

### Pass E — testing, quality, security, performance and execution

Discover commands/config/evidence for:

- development/run and build/package;
- all test types that actually exist in the project, classifying them by the semantic taxonomy in `TEST_STRATEGY.md`;
- lint, formatting verification, type/static analysis, code generation, architecture checks, and coverage policy;
- security tooling/policies such as static checks, dependency/supply-chain checks, secret checks, security test suites, or repository security guidance;
- performance/reliability tooling such as benchmarks, load/stress/endurance checks, profiling, performance budgets, capacity tests, or historical baselines;
- migration/schema/data validation;
- smoke/health and observability checks.

Do not infer that a test/security/performance mechanism exists merely because it is conventional for the language or framework. A category may be `unknown` or `not_detected`.

### Pass F — security and performance baselines

Identify project-defined security constraints, threat-model/security docs, sensitive boundaries, performance budgets/SLOs/SLIs, capacity constraints, benchmark baselines, and known release gates when evidence exists. Store facts, not copied secrets or speculative requirements.

### Pass G — CI/CD and repository automation

Inspect pipeline/workflow definitions, hooks, release automation, deployment configuration, and required checks when available. Separate CI evidence from local commands.

### Pass H — project rules and architecture

Read existing repository instruction files, architecture docs, contributing guides, ADRs, and conventions that materially constrain implementation. Do not silently copy all prose into the Profile; keep project-specific behavioral constraints in `PROJECT_RULES.md` after approval when needed.

### Pass I — executable verification

When safe and inexpensive, use non-destructive commands to corroborate important facts (for example tool versions or declared scripts). Do not install dependencies or mutate the repository merely to improve discovery confidence unless that action is already safe/expected for the project.

## Proposed Profile

Use the structure in `../templates/PROJECT_PROFILE.yaml` and schema semantics in `../schemas/project-profile.schema.json`. Include:

- discovery timestamp if available;
- repository shape/components;
- languages/runtimes/frameworks;
- dependency/package managers;
- persistence/migrations;
- commands and testing/quality/security/performance tooling;
- CI/CD;
- important architecture facts;
- unknowns/conflicts;
- evidence and confidence.

Do not create the file yet. Present a concise discovery report plus the proposed Profile.

## Approval gate

Obtain explicit human approval before writing the first `PROJECT_PROFILE.yaml`. If the human corrects a fact, record the correction as human input and reconcile it with repository evidence rather than erasing the conflict.

After approval, save:

- `.implement-issue/PROJECT_PROFILE.yaml`
- optionally `.implement-issue/DISCOVERY_REPORT.md` for the human-readable snapshot.

Project rules discovered during this pass require their own clear approval if they are going to be persisted as normative rules.
