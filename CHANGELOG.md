# Changelog

All notable changes are documented here.

## 0.3.0 - 2026-09-26

Release-readiness and learning-persistence release.

- Rebranded repository-facing documentation and release artifacts as IssueCraft Workflow.
- Replaced placeholder clone instructions with the real public repository URL.
- Added persistent, human-gated learning ledger and improvement-proposal lifecycle without silent self-modification.
- Extended drift preflight to security tooling/policies, performance budgets/baselines/tooling, and observability evidence.
- Added executable deterministic contract evals for all 16 behavioral scenarios.
- Expanded CI to Linux, macOS, and Windows across two supported Python versions.
- Pinned GitHub Actions to immutable commit SHAs and disabled checkout credential persistence.
- Added Dependabot coverage for GitHub Actions dependencies.
- Hardened release ZIP generation to exclude `.git` metadata and renamed archives to `issuecraft-workflow-<version>.zip`.
- Added release-archive regression tests.
- Improved private security-reporting guidance.
- Fixed bootstrap interview numbering and stale issue-template version text.

## 0.2.1 - 2026-09-26

Documentation/onboarding release.

- Rebuilt the English and Brazilian Portuguese READMEs around a three-step quick start: clone, install, invoke.
- Added first-run examples for existing and empty projects.
- Documented issue lifecycle, AI-provider neutrality, stack neutrality, security, performance, test strategy, manual validation, drift, and continuous improvement in the main README.
- Added update, manual-install, repository-layout, verification, and troubleshooting guidance.
- Hardened release ZIP generation to exclude caches, bytecode, virtual environments, and nested ZIP artifacts.
- Added regression checks for README onboarding content.

## 0.2.0 - 2026-09-26

Security/performance/testing hardening release.

- Added mandatory security-impact triage and secure implementation/validation contract.
- Added mandatory performance-impact triage, baseline/budget handling, and safe measurement contract.
- Added comprehensive risk-based test taxonomy covering functional, regression, robustness, security, performance/reliability, accessibility/compatibility, migration/recovery, and static/build-time verification.
- Added release blockers for known material security regressions and established performance-budget violations unless specifically risk-accepted by a human.
- Extended Project Discovery/Profile/Blueprint to capture testing, security, performance, observability, and related commands/decisions without stack assumptions.
- Added provider-neutrality and stack-neutrality validator invariants.
- Added security/performance/test regression eval scenarios.
- Hardened installer against managed-path symlink redirection.
- Expanded automated repository tests.

## 0.1.0 - 2026-09-26

Initial public version.

- Provider-neutral canonical core.
- Stack/framework/language agnostic Project Discovery.
- Empty-project Project Bootstrap with adaptive human decisions.
- Evidence-backed `PROJECT_PROFILE` and decision-backed `PROJECT_BLUEPRINT`.
- Human approval gates for project context changes and workflow improvement.
- Drift detection.
- Tracker-neutral issue state model.
- `In Progress → In Review → human validation → Done` lifecycle.
- Issue-specific manual validation plan on entry to `In Review`.
- Agent Skill adapters for `.agents/skills` and `.claude/skills`.
- Cross-platform installer and structural validation tests.
