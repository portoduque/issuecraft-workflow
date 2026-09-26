# Architecture

## Separation of concerns

The repository intentionally separates four layers and keeps security/performance/testing as cross-cutting core contracts:

1. **Canonical core (`core/`)** — provider- and stack-neutral behavior.
2. **Project state (`.implement-issue/` in a target project)** — observed Profile, intended Blueprint, local Rules, drift/validation artifacts.
3. **Agent discovery adapters** — tiny `SKILL.md` entry points placed where each agent surface discovers skills.
4. **Maintainer tooling (`scripts/`, `tests/`, `evals/`)** — installation and regression checks for this workflow repository.

## Why Blueprint and Profile are separate

A project can intend to use one technology while the repository implements another. Combining intention and observation into one file creates false certainty.

- `PROJECT_BLUEPRINT.yaml` answers: **What have humans/docs decided should be built?**
- `PROJECT_PROFILE.yaml` answers: **What does current repository evidence show exists?**

Both can be true at the same time even when they disagree. That disagreement becomes drift, not an automatic rewrite.

## Provider-neutral core

The core expresses actions through capabilities such as reading files, executing commands, reading/writing tracker state, or interacting with a runtime. It does not call named vendor tools.

Adapters are discovery shims only. If a new coding agent supports the open Agent Skills format, adding it should normally require only placing the same thin skill entry point in that agent's discovery directory.

## Cross-cutting engineering contracts

`core/TEST_STRATEGY.md`, `core/SECURITY.md`, and `core/PERFORMANCE.md` apply to every issue. They are semantic/risk-based rather than stack-specific:

- every issue performs security-impact and performance-impact triage;
- every issue considers the full test taxonomy and selects applicable tests from repository evidence;
- known material security regressions or established performance-budget violations block review unless specifically risk-accepted by a human;
- test/security/performance tools are discovered, never assumed from a language/framework;
- unavailable evidence is reported as unavailable, never converted into a pass.

## State model

```text
                  ┌───────────────┐
                  │ Project ready │
                  └───────┬───────┘
                          │
                          ▼
                       Todo
                          │
                          ▼
                    In Progress
                          │
                   implement/check
                          │
                          ▼
                     In Review
                          │
                 human validation
                   ┌──────┴──────┐
                   │             │
                 fail           pass
                   │             │
                   ▼             ▼
              In Progress       Done
```

`Done` is deliberately not agent-owned.
