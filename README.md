# Implement Issue Workflow

A reusable, AI-agent-neutral and stack-neutral workflow for implementing software issues with discovery, planning, security, performance, testing, review, and human approval built in.

**Version:** 0.2.1  
**License:** MIT  
**Language:** [English](README.md) · [Português (Brasil)](README.pt-BR.md)

---

## Quick start

You only need **Git**, **Python 3** for the installer, and one supported coding agent.

### 1. Clone this repository

```bash
git clone <REPOSITORY_URL>
cd implement-issue-workflow
```

Replace `<REPOSITORY_URL>` with the GitHub clone URL of this project.

### 2. Install the workflow into your project

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

The installer does **not** change your application stack and does **not** create project decisions automatically. It only installs the workflow runtime and agent entry points.

### 3. Open your project in your coding agent and run the workflow

| Agent | Command |
|---|---|
| Codex | `$implement-issue` |
| Claude Code | `/implement-issue` |
| Antigravity | `/implement-issue` |

Then give it the issue, task, bug, or feature you want implemented.

Example:

```text
/implement-issue
Implement issue #42: add password visibility toggle to the user form.
```

For Codex, use `$implement-issue` instead of `/implement-issue`.

**That is enough to start.** On the first run, the workflow discovers how your project actually works before changing code.

---

## What happens on the first run?

The workflow starts by inspecting the repository instead of assuming a stack.

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

The workflow looks for evidence of:

- languages and runtimes;
- frameworks and major libraries;
- package/dependency managers;
- databases and persistence;
- migration systems;
- test tools and test commands;
- lint, format and type-check commands;
- build and run commands;
- CI/CD configuration;
- security tooling and policies;
- performance tooling, benchmarks and budgets;
- repository architecture and relevant conventions.

It proposes a `PROJECT_PROFILE.yaml` based on evidence.

If something cannot be determined, it remains `unknown` or `not_detected`. The workflow must not invent missing information.

### Empty project

If there is not enough implementation to discover a stack, the workflow enters **Project Bootstrap**.

It:

1. reads any existing documentation;
2. reuses decisions that are already documented;
3. asks a short, adaptive set of questions only for unresolved decisions;
4. leaves undecided items as `undecided`;
5. proposes a `PROJECT_BLUEPRINT.yaml`;
6. waits for human approval before saving it.

The distinction is intentional:

- **Blueprint** = what you intend to build.
- **Profile** = what the repository proves currently exists.

---

## Normal issue flow

After onboarding, every issue follows the same core lifecycle:

```text
issue/task
   ↓
understand context
   ↓
In Progress
   ↓
plan
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

The workflow can move an issue to **In Review**, but **Done is human-owned**. It must not mark an issue Done merely because the agent believes its own implementation is correct.

---

## Why it is stack-neutral

The canonical workflow does not contain project-specific commands such as:

```text
npm test
pytest
mvn test
docker compose up
```

Instead, it discovers the commands actually used by the repository and stores them in project context.

Conceptually, the core asks for things like:

```text
build command
unit-test command
integration-test command
lint command
migration mechanism
database type
CI behavior
```

The project supplies the concrete answers through evidence.

This lets the same workflow operate on web apps, APIs, CLIs, libraries, mobile projects, monorepos, services, or other software projects without embedding one preferred language or framework in the core.

---

## Why it is AI-agent-neutral

There is only **one canonical workflow**:

```text
core/WORKFLOW.md
```

Agent-specific files are thin entry points that delegate to that same core.

```text
Codex ─────────┐
Claude Code ───┼──→ canonical core
Antigravity ───┘
```

The repository includes automated checks that prevent provider-specific behavior from leaking into `core/`.

Current entry points:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

See [`docs/compatibility.md`](docs/compatibility.md) for details.

---

## Security is mandatory

Every issue gets a security-impact triage, even when the issue does not initially appear security-related.

The workflow considers relevant areas such as:

- authentication and authorization;
- permissions and privilege boundaries;
- secrets and credentials;
- sensitive data;
- input validation;
- injection risks;
- file handling;
- network boundaries;
- persistence and data integrity;
- dependencies and supply-chain changes;
- concurrency and state consistency;
- logging and accidental information exposure.

Validation is proportional to the risk of the change. A known material security regression blocks review unless a human explicitly accepts that specific risk.

See [`core/SECURITY.md`](core/SECURITY.md).

---

## Performance is mandatory

Every issue also gets a performance-impact triage.

When relevant, the workflow considers:

- algorithmic complexity;
- database queries and I/O;
- network calls;
- memory use;
- CPU use;
- concurrency and locks;
- cache behavior;
- payload sizes;
- startup/build cost;
- resource leaks;
- existing performance budgets and baselines.

It uses real project baselines when available and must not invent performance thresholds.

Expensive or destructive load/stress testing must not be run against production without explicit authorization.

See [`core/PERFORMANCE.md`](core/PERFORMANCE.md).

---

## Testing strategy

The workflow does **not** blindly run every possible test type. It considers the complete test space and selects what is applicable to the risks introduced by the issue.

Depending on the project and change, that can include:

- unit tests;
- component tests;
- integration tests;
- contract tests;
- API tests;
- system tests;
- end-to-end tests;
- acceptance tests;
- smoke and sanity tests;
- regression tests;
- negative and boundary tests;
- property-based tests;
- fuzz tests;
- mutation tests;
- concurrency, race, locking and idempotency tests;
- resilience and fault-injection tests;
- security tests;
- benchmarks;
- load, stress, spike and soak tests;
- accessibility tests;
- visual regression tests;
- compatibility tests;
- install, upgrade, downgrade and rollback tests;
- migration and data-integrity tests;
- backup, restore and recovery tests;
- static analysis, lint, type checking and build validation.

The result of a test category must remain explicit:

```text
pass
fail
not_applicable
unavailable
```

`not_applicable` and `unavailable` are never treated as `pass`.

For reproducible bug fixes, the preferred flow is to create or identify a regression reproducer that fails before the fix and passes after it whenever practical.

See [`core/TEST_STRATEGY.md`](core/TEST_STRATEGY.md).

---

## Manual validation before Done

When implementation and automated validation are complete, the workflow generates a manual validation plan tailored to the issue.

It should contain, when applicable:

- prerequisites;
- test data;
- exact actions;
- expected results;
- edge cases;
- regression checks;
- security-sensitive checks;
- performance-sensitive checks;
- cleanup steps.

It must not produce a vague checklist such as “check if it works.”

The issue then enters **In Review**. A human performs the validation and decides whether it can become **Done**.

---

## Project drift detection

Projects change over time. The workflow therefore does not assume the original Profile is permanently correct.

On later runs, it performs a lightweight drift check against important evidence.

Example:

```text
PROJECT_PROFILE says:
package manager = A

repository now shows:
lockfile for B
manifest declares B
old lockfile removed

→ possible drift detected
→ proposed Profile update
→ human approval required
```

It never silently rewrites approved project knowledge.

See [`core/DRIFT_DETECTION.md`](core/DRIFT_DETECTION.md).

---

## Continuous improvement without silent self-modification

The workflow can learn from repeated use, but it does not silently modify itself.

If it discovers a reusable improvement, it can generate a structured proposal containing:

- the problem;
- evidence;
- current behavior;
- proposed behavior;
- whether the learning is generic or project-specific;
- expected benefit;
- risks/trade-offs;
- suggested regression coverage.

Only after human approval should a persistent workflow or project rule be changed.

This prevents one project's conventions from contaminating the generic workflow.

See [`core/CONTINUOUS_IMPROVEMENT.md`](core/CONTINUOUS_IMPROVEMENT.md).

---

## What the installer adds to your project

Running:

```bash
python scripts/install.py /path/to/your-project
```

adds:

```text
your-project/
├── .agents/
│   └── skills/
│       └── implement-issue/
│           └── SKILL.md
├── .claude/
│   └── skills/
│       └── implement-issue/
│           └── SKILL.md
└── .implement-issue/
    └── system/
        ├── core/
        ├── schemas/
        ├── templates/
        ├── manifest.json
        └── VERSION
```

It does **not** pre-create:

```text
PROJECT_PROFILE.yaml
PROJECT_BLUEPRINT.yaml
PROJECT_RULES.md
```

Those are project-owned state and require the workflow's evidence/decision process and human approval.

The target project does not become a Python project. Python is only used by this repository's installer.

---

## Updating an existing installation

Pull or download the newer workflow release, then run:

```bash
python scripts/install.py /path/to/your-project --overwrite-system
```

This replaces the workflow runtime and adapters while preserving project-owned state such as approved Profile, Blueprint, Rules, validation artifacts, and improvement proposals.

---

## Installing without Python

Python is only a convenience for copying the runtime. Manual installation is supported.

Copy:

```text
core/      → <project>/.implement-issue/system/core/
schemas/   → <project>/.implement-issue/system/schemas/
templates/ → <project>/.implement-issue/system/templates/
VERSION    → <project>/.implement-issue/system/VERSION
manifest.json → <project>/.implement-issue/system/manifest.json

.agents/skills/implement-issue/
    → <project>/.agents/skills/implement-issue/

.claude/skills/implement-issue/
    → <project>/.claude/skills/implement-issue/
```

Do not create a Profile or Blueprint from the templates manually just to skip onboarding.

---

## Repository structure

```text
implement-issue-workflow/
├── core/                 # canonical provider/stack-neutral behavior
├── schemas/              # Profile and Blueprint contracts
├── templates/            # generated-artifact templates
├── docs/                 # architecture, installation and examples
├── evals/                # behavioral regression scenarios
├── tests/                # repository/invariant tests
├── scripts/              # installer, validator and release tooling
├── .agents/skills/       # Codex/Antigravity entry point
├── .claude/skills/       # Claude Code entry point
├── manifest.json
├── VERSION
└── README.md
```

The most important file is [`core/WORKFLOW.md`](core/WORKFLOW.md). It is the canonical execution contract.

---

## Verify this repository

Before publishing or modifying the workflow, run:

```bash
python scripts/validate_repo.py
python -m unittest discover tests -v
```

These checks validate structural contracts including provider neutrality, stack neutrality, quality contracts, adapters, installer safety, schemas, and regression coverage.

---

## Troubleshooting

### The agent does not see `implement-issue`

1. Confirm you installed the workflow into the same repository/workspace opened by the agent.
2. Confirm one of these files exists:

```text
.agents/skills/implement-issue/SKILL.md
.claude/skills/implement-issue/SKILL.md
```

3. Restart/reopen the coding agent if it caches project skills.
4. Use the explicit command for your agent from the compatibility table above.

### The installer says the workflow already exists

Use the update mode:

```bash
python scripts/install.py /path/to/your-project --overwrite-system
```

### I already have `.agents/` or `.claude/`

That is fine. The installer only manages the `implement-issue` skill directory inside those locations.

### My repository is empty

That is supported. Run the workflow normally. It will use Project Bootstrap instead of pretending it discovered a stack.

### My project uses an unusual language/framework/tool

That is supported by design. The workflow should derive its behavior from repository evidence and project commands rather than from a fixed allowlist of technologies.

---

## More documentation

Start here only if you need deeper details:

- [Installation](docs/install.md)
- [Architecture](docs/architecture.md)
- [Agent compatibility](docs/compatibility.md)
- [Project-owned files](docs/project-files.md)
- [Security, performance and testing baseline](docs/security-quality-baseline.md)
- [Existing-project example](docs/examples/existing-project.md)
- [Empty-project example](docs/examples/empty-project.md)
- [Drift example](docs/examples/drift.md)

---

## Contributing

Contributions are welcome. Changes to the canonical workflow should preserve:

- provider neutrality;
- stack/language/framework neutrality;
- evidence before assumptions;
- human approval gates;
- security and performance triage;
- comprehensive risk-based validation;
- human ownership of Done.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## License

MIT. See [`LICENSE`](LICENSE).
