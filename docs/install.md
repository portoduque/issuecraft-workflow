# Installation

For most users, installation is three steps.

## 1. Clone the workflow repository

```bash
git clone <REPOSITORY_URL>
cd implement-issue-workflow
```

## 2. Install it into the target repository

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

The installer uses only the Python standard library. Python is needed only to copy the workflow files; the target application does not become a Python project and does not require Python after installation.

## 3. Invoke the skill in the target repository

- Codex: `$implement-issue`
- Claude Code: `/implement-issue`
- Antigravity: `/implement-issue`

On first use, the workflow performs Project Discovery or Project Bootstrap before implementation.

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

The installer does not create `PROJECT_PROFILE.yaml`, `PROJECT_BLUEPRINT.yaml`, or `PROJECT_RULES.md`. Project-owned state is created only by the workflow after the appropriate evidence/decision process and human approval.

## Update

After pulling/downloading a newer workflow version:

```bash
python scripts/install.py /path/to/target-repository --overwrite-system
```

This updates only the installed runtime/adapters and preserves project-owned state.

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

Do not pre-create a Profile or Blueprint from templates to bypass onboarding.
