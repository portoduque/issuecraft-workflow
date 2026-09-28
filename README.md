# IssueCraft Workflow

[![CI](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/portoduque/issuecraft-workflow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-agent-neutral and stack-neutral workflow for implementing software issues from project discovery to human validation.

**Version:** 0.16.0  
**License:** MIT  
**Language:** [English](README.md) · [Português (Brasil)](README.pt-BR.md)

## Quick start

You need **Git**, **Python 3** for installation, and a compatible coding agent.

### 1. Clone

```bash
git clone https://github.com/portoduque/issuecraft-workflow.git
cd issuecraft-workflow
```

### 2. Install into your project

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

### 3. Run `implement-issue`

| Agent | Command |
|---|---|
| Codex | `$implement-issue` |
| Claude Code | `/implement-issue` |
| Antigravity | `/implement-issue` |

Example:

```text
/implement-issue
Implement issue #42: add a password visibility toggle.
```

For Codex, use `$implement-issue`.

That is enough to start. On first use, IssueCraft learns how the repository actually works before changing application code.

## What happens on the first run

For an existing project, IssueCraft discovers the real repository from evidence: languages, runtimes, frameworks, dependencies, persistence/migrations, test commands, coverage policy, lint/type/build checks, CI, security, performance and architecture.

It proposes a `PROJECT_PROFILE` and asks before persisting it.

For an empty or near-empty project, it uses a short adaptive interview and proposes a `PROJECT_BLUEPRINT` instead of inventing a stack.

Later runs detect material drift and update project knowledge only through the applicable human gate.

## Issue flow

```text
issue
  ↓
discover/reconcile project context
  ↓
plan from evidence
  ↓
implement smallest coherent change
  ↓
security + performance impact triage
  ↓
applicable automated validation
  ↓
In Review
  ↓
MANUAL_VALIDATION_PLAN.md
  ↓
human validation
  ↓
PASS → Done
FAIL → back to implementation
PARTIAL / NOT RUN → remain In Review
```

The agent cannot mark the issue `Done` merely because automated tests passed or because the agent exercised the UI itself.

## Testing and code coverage

IssueCraft considers the full semantic test space and runs/adds the types that are applicable to the changed behavior and available project infrastructure.

This can include unit, component, integration, contract, API, system, end-to-end, acceptance, smoke, regression, negative/boundary, property-based, fuzz, mutation, concurrency, resilience, security, benchmark/load/stress/soak, accessibility, compatibility, migration/recovery, lint, type/static analysis and build/package checks.

For materially changed behavior, evidence must identify a meaningful check/assertion; a green broad suite or a high coverage percentage alone is not proof.

Code coverage is also a quality guard:

- discover the project's existing coverage command/tool/policy;
- preserve established thresholds/baselines;
- do not lower or bypass coverage merely to make a change pass;
- directly cover materially new/changed executable behavior when viable;
- if the project has no coverage tooling, do not silently install one or invent a universal percentage.

The detailed rules live in [core/TEST_STRATEGY.md](core/TEST_STRATEGY.md) and [docs/testing.md](docs/testing.md).

Security and performance remain mandatory impact analyses; see [core/SECURITY.md](core/SECURITY.md) and [core/PERFORMANCE.md](core/PERFORMANCE.md).

## Manual validation before Done

After automated validation, IssueCraft generates:

```text
.implement-issue/issues/<issue-key>/MANUAL_VALIDATION_PLAN.md
```

IssueCraft resolves `<issue-key>` from the current issue/reference and reports the exact artifact path in the handoff.

The final human step is:

1. Open the reported `.implement-issue/issues/<issue-key>/MANUAL_VALIDATION_PLAN.md`.
2. Confirm the listed prerequisites/setup.
3. Execute each numbered scenario in order.
4. Compare each action with its expected result.
5. Run the listed regression/security/performance/accessibility/compatibility/migration/recovery checks when applicable.
6. Record one result: **PASS**, **FAIL**, or **PARTIAL / NOT RUN**.
7. If **FAIL**, provide the failing step, expected result and actual result; IssueCraft returns to implementation and revalidates.
8. Only an explicit human **PASS** (or equivalent clear approval) allows the transition from `In Review` to `Done`.

See [docs/validation.md](docs/validation.md) for the full handoff model.

## AI-agent neutral

There is one canonical workflow:

```text
core/WORKFLOW.md
```

Agent-specific files are thin adapters only:

```text
.agents/skills/implement-issue/SKILL.md   # Codex + Antigravity
.claude/skills/implement-issue/SKILL.md  # Claude Code
```

Provider-specific behavior must not leak into `core/`. Compatibility details are in [docs/compatibility.md](docs/compatibility.md).

## Stack/language neutral

IssueCraft discovers the target project instead of assuming Python, JavaScript, Java, a database, a framework or a test runner.

Commands and tools come from repository evidence and approved project context. Monorepos and multi-service repositories are handled per component when needed.

## Parallel work

Multiple agents/issues may run in parallel, but mutating executions should use isolated physical workspaces/checkouts when the environment supports them.

IssueCraft does **not** run a lock server, scheduler, heartbeat, agent registry, auto-worktree, auto-rebase or auto-merge. It keeps operational artifacts per issue, re-reads project-scoped state visible in the current workspace/integration point before approved concurrent writes, treats overlap as risk rather than automatic dependency, and selectively invalidates stale validation when the integration base changes. A new worktree must have the IssueCraft runtime/adapters available there; local uncommitted state from another worktree is not assumed to be shared.

See [docs/parallel-work.md](docs/parallel-work.md).

## Controlled learning

IssueCraft can learn from real use, but it never silently rewrites its own rules.

```text
observe evidence
  ↓
draft proposal
  ↓
human approval to persist
  ↓
.implement-issue/proposals/WIP-*.md
  ↓
optional LEARNINGS.md record
  ↓
separate human approval to adopt
```

A proposal or `LEARNINGS.md` entry is historical evidence, not automatically normative behavior.

See [docs/learning.md](docs/learning.md) and [core/CONTINUOUS_IMPROVEMENT.md](core/CONTINUOUS_IMPROVEMENT.md).

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

Shared project knowledge such as `PROJECT_PROFILE.yaml`, `PROJECT_BLUEPRINT.yaml`, `PROJECT_RULES.md`, `LEARNINGS.md` and proposals remains project-scoped. Handoff, manual validation and execution-report artifacts are issue-scoped under `.implement-issue/issues/<issue-key>/`.

## Update IssueCraft in a project

```bash
git pull
python scripts/install.py /path/to/your-project --overwrite-system
```

`--overwrite-system` replaces only IssueCraft runtime/adapters and preserves project-owned state.

Manual installation without Python is documented in [docs/install.md](docs/install.md).

## Verify this repository

Run the deterministic validation layers:

```bash
python scripts/validate_repo.py
python scripts/run_evals.py
python scripts/run_live_evals.py validate
python -m unittest discover tests -v
```

For IssueCraft's own branch-aware code-coverage gate:

```bash
python -m pip install -r requirements-dev.txt
python -m coverage erase
python -m coverage run --branch --source=scripts -m unittest discover tests -v
python -m coverage run --append --branch --source=scripts scripts/validate_repo.py
python -m coverage run --append --branch --source=scripts scripts/run_evals.py
python -m coverage run --append --branch --source=scripts scripts/run_live_evals.py validate
python -m coverage report --show-missing --fail-under=90
```

CI runs the main suite across Linux, macOS and Windows and enforces the coverage gate separately.

## Documentation

- [Installation](docs/install.md)
- [Architecture](docs/architecture.md)
- [Agent compatibility](docs/compatibility.md)
- [Release compatibility smoke checks](docs/compatibility-release.md)
- [Testing and coverage](docs/testing.md)
- [Manual validation and Done gate](docs/validation.md)
- [Parallel work safety](docs/parallel-work.md)
- [Controlled learning](docs/learning.md)
- [Project runtime files](docs/project-files.md)

## Troubleshooting

If the agent does not see `implement-issue`, confirm the adapter exists in the target repository and restart/reload the agent workspace if its skill discovery requires it.

If the runtime already exists, update with `--overwrite-system`.

If a discovered project fact is wrong, correct the proposal before approving it. IssueCraft must preserve evidence/conflicts rather than silently inventing facts.

If an applicable test cannot run, IssueCraft reports it as `unavailable`; it does not convert that state into `pass`.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Generic behavior changes should include regression/eval evidence and preserve provider/stack neutrality.

## License

MIT. See [LICENSE](LICENSE).
