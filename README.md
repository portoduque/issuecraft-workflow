# IssueCraft Workflow

[![CI](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A reusable, AI-agent-neutral and stack-neutral workflow for implementing software issues from project discovery to human validation, with security, performance, testing, drift detection, and controlled learning built in.

**Version:** 0.9.0  
**License:** MIT  
**Language:** [English](README.md) · [Português (Brasil)](README.pt-BR.md)

---

## Quick start

You need **Git**, **Python 3** for installation, and a compatible coding agent.

### 1. Clone IssueCraft

```bash
git clone https://github.com/portoduque/issuecraft-workflow.git
cd issuecraft-workflow
```

### 2. Install it into your project

```bash
python scripts/install.py /path/to/your-project
```

Examples:

```bash
# Linux/macOS
python scripts/install.py ~/projects/my-app

# Windows
python scripts/install.py C:\dev\my-app
```

The installer copies only the workflow runtime and agent entry points. It does **not** change your application's stack and does **not** pre-create project decisions.

### 3. Invoke `implement-issue`

| Agent | Command |
|---|---|
| Codex | `$implement-issue` |
| Claude Code | `/implement-issue` |
| Antigravity | `/implement-issue` |

Example:

```text
/implement-issue
Implement issue #42: add a password visibility toggle to the user form.
```

For Codex, use `$implement-issue` instead of `/implement-issue`.

**That is enough to start.** On the first run, IssueCraft learns how the repository actually works before changing application code.

---

## What IssueCraft does

IssueCraft provides one canonical `implement-issue` workflow that:

- discovers an existing project's real languages, frameworks, package/dependency management, database, migrations, tests, CI, lint, build, security and performance tooling from evidence;
- bootstraps empty projects through a short adaptive interview instead of inventing a stack;
- creates a proposed `PROJECT_PROFILE` for observed reality or `PROJECT_BLUEPRINT` for planned architecture;
- requires human approval before persisting important project knowledge;
- detects project drift on later runs;
- plans and implements the smallest coherent issue change;
- models material behavior changes as current contract → requested delta → resulting contract, preserving unspecified existing obligations;
- performs mandatory security-impact and performance-impact triage;
- selects tests by risk instead of assuming one framework or one test command;
- requires evidence-or-zero for material obligations, decomposes compound requirements, and uses targeted discrimination checks when test strength is materially uncertain;
- keeps scope integrity: local/reversible replanning stays autonomous, while material issue intent/scope drift requires a human decision;
- moves work through `In Progress → In Review → human validation → Done`;
- generates an issue-specific manual validation plan before `In Review`;
- learns from real usage while keeping persistence and adoption human-controlled.

---

## Compact output, full evidence

IssueCraft keeps the analysis and validation deep while keeping chat handoffs short.

The rule is:

> **Compress presentation, never evidence.**

Detailed evidence stays in durable project artifacts such as the Profile, drift report, validation plan, execution report, or improvement proposal. In chat, IssueCraft focuses on the current state, material changes, failures/unavailable checks, residual risks, required human decision, and the next action.

Routine successful checks may be grouped; `not_applicable` checks may be summarized. Failures, unavailable validation, security/performance risks, uncertainty, and human gates are never hidden to save tokens.

Compact output is a **projection of the complete validation result**, never a reason to validate fewer obligations. Partial evidence stays partial: if some material members are not proven, the parent obligation is not reported as a full pass.

This reduces repeated output and accumulated conversation context without reducing testing or engineering depth.

---

## First run: existing project vs. empty project

```text
first run
   ↓
inspect repository
   ↓
┌───────────────────────┬─────────────────────────┐
│ existing project      │ empty/new project       │
│                       │                         │
│ Project Discovery     │ Project Bootstrap       │
│                       │                         │
│ proposed Profile      │ proposed Blueprint      │
└───────────┬───────────┴────────────┬────────────┘
            │                        │
            └──── human approval ────┘
                         ↓
                  implement issue
```

### Existing project

IssueCraft inspects repository evidence for:

- languages, runtimes, frameworks and major libraries;
- dependency/package managers and workspaces;
- persistence, databases and migrations;
- unit, integration, contract, system, E2E and other existing tests;
- lint, format, type/static analysis and build commands;
- CI/CD and release automation;
- security policies/tooling and trust boundaries;
- performance tooling, budgets, baselines and capacity evidence;
- architecture, modules/services and project conventions.

It proposes `.implement-issue/PROJECT_PROFILE.yaml`.

If a fact cannot be established, it remains `unknown` or `not_detected`. Absence of evidence is not silently converted into a project fact.

### Empty or near-empty project

IssueCraft does not pretend to discover a stack that does not exist.

It reads any existing documentation first, asks only the unresolved questions needed for the current scaffold, keeps optional decisions `undecided`, and proposes `.implement-issue/PROJECT_BLUEPRINT.yaml`.

The distinction is intentional:

- **Blueprint** = intended design.
- **Profile** = observed repository reality.

Both are human-approved before persistence.

---

## Issue lifecycle

```text
issue/task
   ↓
understand context
   ↓
In Progress
   ↓
plan from evidence
   ↓
implement
   ↓
security review
   ↓
performance review
   ↓
risk-based automated validation
   ↓
generate manual validation plan
   ↓
In Review
   ↓
human validation
   ├── failed → In Progress
   └── passed → Done
```

IssueCraft may prepare an issue for `In Review`, but **Done is human-owned**. Automated checks, an agent's own UI interaction, or confidence in the diff never substitute for the final human validation gate.

During implementation, context is retrieved progressively: IssueCraft follows high-signal code/contracts/tests until material information gaps are resolved instead of reading the repository exhaustively. If repeated fixes fail without new evidence, it performs a diagnostic reset before another edit.

For non-trivial multi-surface work, IssueCraft prefers thin verifiable increments and resolves plan-invalidating uncertainty early with risk-first slices. When correctness depends on version-sensitive external behavior that the repository cannot establish, it checks the detected version against narrow authoritative documentation and marks anything it cannot verify as unverified.

Validation is evidence-aware: a prior green result is reused only while its relevant inputs remain materially unchanged. Before `In Review`, IssueCraft also reviews whether the diff weakened the project's quality bar, whether coexistence-sensitive migrations use a compatibility-safe expand/migrate/contract sequence, and whether dependency changes are supported by resolved lock-state and relevant release/migration evidence.

If work is interrupted, IssueCraft can write a compact `.implement-issue/HANDOFF.md`. The handoff is only a resume hypothesis: on the next session it is reconciled against current repository/VCS state, tracker state when available, and durable validation evidence before any edit. Current evidence wins over stale narrative.

Materially hard-to-reverse implementation choices that are not already determined by the issue, approved project knowledge, existing contracts, or unavoidable constraints are treated as one-way doors and require an explicit human decision. Ordinary reversible implementation choices remain autonomous.

For material behavior changes, IssueCraft distinguishes what is **added, modified, removed, renamed/preserved, and unchanged-but-at-risk**. Modified behavior carries preservation obligations for existing scenarios/fields/states/paths the issue did not explicitly remove; removed behavior is verified as absent rather than treated as something to restore.

Before `In Review`, a change-coherence review reconciles the issue and acceptance criteria, project/repository contracts, behavior delta, implementation diff, automated evidence, and manual validation plan. Every material diff change needs a traceable reason. If the implementation plan proves wrong but the issue's intended outcome is unchanged, IssueCraft replans autonomously; if the issue itself would become materially different work, the human decides.

At resume and other material phase transitions, IssueCraft re-reads the mutable authoritative inputs needed for the next decision instead of trusting stale conversation memory. External/reference repositories or specification sources may inform the work, but read access never implies mutation authorization.

---

## AI-agent neutral by design

There is one canonical workflow:

```text
core/WORKFLOW.md
```

Agent-specific files are thin entry points that delegate to the same core:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

The canonical core is not allowed to branch behavior by AI provider. Repository validation scans the core for provider leakage, and the two adapters must remain behaviorally identical.

See [docs/compatibility.md](docs/compatibility.md).

---

## Stack, framework and language neutral

The core works with semantic concepts such as:

```text
build command
test commands
migration mechanism
persistence type
security checks
performance checks
CI behavior
```

It does not hardcode one preferred package manager, framework, database, migration tool, test library or operating system. Concrete commands come from repository evidence and approved project context.

Monorepos and multi-service repositories are discovered per component instead of being forced into one global stack.

---

## Security is mandatory

Every issue gets a security-impact triage, even if the issue title does not look security-related.

When applicable, IssueCraft considers authentication/authorization, tenant or privilege boundaries, untrusted input, secrets, sensitive data, files, network trust, persistence, dependency/supply-chain changes, state transitions, concurrency, logging, and other changed attack surfaces.

A known material security regression blocks `In Review` unless that **specific residual risk** is explicitly accepted by a human.

IssueCraft does not claim absolute security. It records what was assessed, what actually ran, and what remains unverified.

See [core/SECURITY.md](core/SECURITY.md).

---

## Performance is mandatory

Every issue also gets a performance-impact triage.

When relevant, IssueCraft considers algorithmic work, database/storage I/O, network calls, memory/resources, concurrency/locks, caching, payloads, startup/build cost, client responsiveness, background processing and observability volume.

Existing budgets and baselines are respected when found. Numeric thresholds are never invented.

High-load or destructive testing against production/shared systems requires explicit authorization.

See [core/PERFORMANCE.md](core/PERFORMANCE.md).

---

## Comprehensive risk-based testing

IssueCraft considers the full semantic test space but runs/adds only what is applicable to the change and available in the project.

That can include unit, component, integration, contract, API/interface, system, end-to-end, acceptance, smoke, regression, negative/boundary, property-based, fuzz, mutation, concurrency/race/idempotency, resilience/fault-injection, security, benchmark, load, stress, spike, soak, accessibility, visual regression, compatibility, migration, recovery, lint, typecheck and build verification.

Every selected check keeps an explicit result:

```text
pass
fail
not_applicable
unavailable
```

`not_applicable` and `unavailable` never mean `pass`.

For reproducible bugs, IssueCraft prefers a durable regression reproducer that fails before the fix and passes after it when feasible. That RED is valid only when the intended defect/invariant actually causes the failure.

IssueCraft also traces materially changed behaviors and acceptance criteria to meaningful evidence, chooses the lowest-cost test layer that can faithfully prove them, checks assertion quality rather than raw test count, and inspects risk-relevant equivalent paths/sibling surfaces after understanding a root cause. Mocks/fakes must preserve the contract under test; expensive E2E is reserved for real cross-layer risk.

Coverage follows **evidence-or-zero**: a material obligation is not considered proven merely because a related suite is green. Compound requirements are decomposed into independently falsifiable clauses/fields/cases, vague requirements become explicit verification-precision gaps instead of invented thresholds, and an applicable check is labeled `unavailable` only after a safe probe or other concrete capability/environment evidence. For high-risk or uncertain assertions, IssueCraft may use an isolated fault/mutation discrimination check to confirm the verification can actually detect the wrong behavior; this is risk-based, not mandatory for every issue.

See [core/TEST_STRATEGY.md](core/TEST_STRATEGY.md).

---

## Manual validation before Done

When automated validation is complete, IssueCraft generates:

```text
.implement-issue/MANUAL_VALIDATION_PLAN.md
```

The plan is derived from the issue, acceptance criteria, actual diff, affected code, project rules and automated results. It includes exact prerequisites, actions and expected results plus relevant regression, security, performance, accessibility, compatibility, migration and cleanup checks.

It must not degrade into a generic "check that it works" checklist.

---

## Drift detection

An approved Profile is not assumed to stay correct forever.

On later runs, IssueCraft performs a cheap preflight over evidence that can change engineering behavior: manifests, lockfiles, runtimes, frameworks, test/build commands, security policies/tooling, performance budgets/baselines/tooling, observability, persistence/migrations, CI and architecture boundaries.

Material differences become a drift proposal. IssueCraft does not silently rewrite the Profile.

See [core/DRIFT_DETECTION.md](core/DRIFT_DETECTION.md).

---

## Controlled learning over time

IssueCraft can learn from real use without becoming a silently self-modifying system.

At the end of an issue it can identify reusable evidence such as a missed edge case, validation gap, project convention, security/performance escape, or adapter limitation.

The workflow separates:

```text
observe
  ↓
draft proposal
  ↓
human approval to persist
  ↓
.implement-issue/proposals/WIP-*.md
  ↓
optional approved learning record
  ↓
.implement-issue/LEARNINGS.md
  ↓
separate human approval to adopt behavior
```

A persisted proposal or entry in `LEARNINGS.md` is **not automatically normative**. Adoption into `PROJECT_RULES`, Profile/Blueprint, an adapter or the canonical core requires the appropriate human decision.

Recurrence across independent issues/features can strengthen the evidence for a proposal, but recurrence never auto-promotes a learning into persistent or normative behavior.

This prevents one project's habits from contaminating the generic workflow.

Generic IssueCraft changes also pass an anti-bloat admission check: concrete gap/evidence, overlap review, merge-first preference, true cross-project generality, ongoing complexity/context cost, and regression proof. Popularity or novelty alone is not enough.

Canonical rules must also describe portable engineering procedures rather than workarounds for one agent/runtime quirk; implementation-specific behavior stays in compatibility/adapters/evals until a generic need is demonstrated.

See [core/CONTINUOUS_IMPROVEMENT.md](core/CONTINUOUS_IMPROVEMENT.md).

---

## What gets installed

```text
your-project/
├── .agents/skills/implement-issue/SKILL.md
├── .claude/skills/implement-issue/SKILL.md
└── .implement-issue/
    └── system/
        ├── core/
        ├── schemas/
        ├── templates/
        ├── manifest.json
        └── VERSION
```

IssueCraft does **not** pre-create `PROJECT_PROFILE`, `PROJECT_BLUEPRINT`, `PROJECT_RULES.md`, `LEARNINGS.md`, persistent proposals, or `HANDOFF.md`. Persistent project knowledge follows the appropriate human gate; `HANDOFF.md` is created only when unfinished work actually needs resumable state.

---

## Updating IssueCraft in a project

Update this repository, then reinstall only the runtime:

```bash
git pull
python scripts/install.py /path/to/your-project --overwrite-system
```

`--overwrite-system` replaces the installed IssueCraft runtime/adapters while preserving project-owned state under `.implement-issue/`.

---

## Install without Python

Python is only the convenience installer. Manual installation is documented in [docs/install.md](docs/install.md).

---

## Verify the repository

Run the same deterministic layers used by CI:

```bash
python scripts/validate_repo.py
python scripts/run_evals.py
python scripts/run_live_evals.py validate
python -m unittest discover tests -v
```

CI runs these on Linux, macOS and Windows.

The 40 scenario files in `evals/scenarios/` have executable provider-neutral contract assertions. Optional live-agent evals may also be run in sandbox repositories, but they are not made a canonical dependency on one AI provider.

---

## Repository structure

```text
issuecraft-workflow/
├── core/                 # canonical provider/stack-neutral behavior
├── schemas/              # Profile and Blueprint contracts
├── templates/            # generated/project-state templates
├── docs/                 # installation, architecture and examples
├── evals/                # behavioral scenarios
├── tests/                # repository/invariant tests
├── scripts/              # installer, validator, eval runner, release tooling
├── .agents/skills/       # Codex/Antigravity entry point
├── .claude/skills/       # Claude Code entry point
├── manifest.json
├── VERSION
└── README.md
```

The normative execution contract is [core/WORKFLOW.md](core/WORKFLOW.md).

---

## Troubleshooting

### The agent does not see `implement-issue`

Confirm the workflow was installed into the same repository/workspace opened by the agent and that the appropriate skill file exists:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

Restart/reload the agent workspace if its skill discovery is cached.

### The runtime is already installed

Use:

```bash
python scripts/install.py /path/to/your-project --overwrite-system
```

Project-owned state is preserved.

### A first-run fact is wrong

Do not approve the proposed Profile/Blueprint as-is. Correct the fact, provide the evidence if needed, and let IssueCraft reconcile the proposal before persistence.

### A test cannot run

IssueCraft should safely probe the check or its prerequisite/capability when reasonable, then report it as `unavailable` with evidence and use the strongest safe alternative. It must not report a false pass or run a destructive/high-load action merely to prove unavailability.

---

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Generic behavior changes should include a concrete scenario and deterministic regression/eval coverage.

Security reports should follow [SECURITY.md](SECURITY.md).

## License

MIT — see [LICENSE](LICENSE).
