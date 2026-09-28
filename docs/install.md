# Installation

IssueCraft installs a reusable `implement-issue` workflow into another repository. It does not change that repository's application stack.

## Fastest path

### 1. Clone IssueCraft

```bash
git clone https://github.com/portoduque/issuecraft-workflow.git
cd issuecraft-workflow
```

### 2. Install it into the target repository

```bash
python scripts/install.py /path/to/target-repository
```

Examples:

```bash
# Linux/macOS
python scripts/install.py ~/projects/my-app

# Windows
python scripts/install.py C:\dev\my-app
```

The installer uses only the Python standard library. Python is needed only to copy IssueCraft's runtime; the target application does not become a Python project.

### 3. Invoke the skill in the target repository

- Codex: `$implement-issue`
- Claude Code: `/implement-issue`
- Antigravity: `/implement-issue`

On first use, IssueCraft performs Project Discovery or Project Bootstrap before implementation.

## What gets installed

```text
<target>/
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

The installer does not create `PROJECT_PROFILE.yaml`, `PROJECT_BLUEPRINT.yaml`, `PROJECT_RULES.md`, `LEARNINGS.md`, persistent proposals, or issue-execution artifacts. Project-owned state is created only after the relevant workflow process and human approval. Issue-specific `HANDOFF.md`, `MANUAL_VALIDATION_PLAN.md`, and `ISSUE_EXECUTION_REPORT.md` live under `.implement-issue/issues/<issue-key>/` when needed.

## Update

After pulling/downloading a newer IssueCraft version:

```bash
python scripts/install.py /path/to/target-repository --overwrite-system
```

This replaces only the installed runtime/adapters. It preserves project-owned state under `.implement-issue/`.

## Installer help

```bash
python scripts/install.py --help
```

## Manual installation

If Python is unavailable, copy:

- `core/` → `.implement-issue/system/core/`
- `schemas/` → `.implement-issue/system/schemas/`
- `templates/` → `.implement-issue/system/templates/`
- `VERSION` → `.implement-issue/system/VERSION`
- `manifest.json` → `.implement-issue/system/manifest.json`
- `.agents/skills/implement-issue/` → target `.agents/skills/implement-issue/`
- `.claude/skills/implement-issue/` → target `.claude/skills/implement-issue/`

Do not pre-create a Profile, Blueprint, Rules file, learning ledger, proposal, or HANDOFF snapshot merely to bypass human-gated onboarding or simulate interrupted work. `HANDOFF.md` is created under the current issue key only when unfinished work actually needs resumable state.
