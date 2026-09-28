# Agent compatibility release smoke

## Setup

IssueCraft's canonical core is provider-neutral, while Codex, Claude Code, and Antigravity discover/invoke skills through host-specific adapters. External hosts can change independently of IssueCraft.

## Must

- Keep host-specific discovery/invocation details outside canonical core.
- Maintain a disposable release-smoke procedure for Codex, Claude Code, and Antigravity.
- Distinguish structural adapter validation from an actually executed live host smoke.
- Use the provider-neutral live-eval runner-adapter boundary for executable smoke scenarios when configured.
- Record host/version and actual discovery/invocation outcome when claiming live compatibility verification.

## Must not

- Add provider SDKs or provider-specific branches to canonical core just to run compatibility checks.
- Claim live compatibility was verified when only repository structure was checked.
- Run compatibility smoke against production data or non-isolated user state.
