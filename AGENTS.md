# IssueCraft repository maintenance instructions

This repository is the canonical source for the `implement-issue` workflow.

- Keep `core/` provider-neutral. Do not mention specific AI products there.
- Keep stack/framework/language-specific examples out of normative core rules.
- `.agents/skills/implement-issue/SKILL.md` and `.claude/skills/implement-issue/SKILL.md` are thin adapters and should remain behaviorally identical.
- Human gates must not be weakened silently.
- Security-impact triage, performance-impact triage, and comprehensive risk-based test selection are canonical invariants.
- Output efficiency is a canonical invariant: compress presentation, never evidence; durable artifacts hold detail while chat handoffs surface material deltas, failures/risks, gates, and next action.
- Continuous-learning persistence and adoption require explicit human approval.
- Keep `core/SECURITY.md`, `core/PERFORMANCE.md`, and `core/TEST_STRATEGY.md` provider- and stack-neutral.
- New generic behavior should be backed by a deterministic contract eval and, where practical, a repository test.
- When a behavior depends on actual agent execution rather than source text alone, add/update a disposable fixture scenario under `evals/live/`; do not add provider-specific logic to `core/`.
- GitHub Actions dependencies must stay pinned to immutable commit SHAs.
- Run `python scripts/validate_repo.py`, `python scripts/run_evals.py`, `python scripts/run_live_evals.py validate`, and `python -m unittest discover tests -v` before considering a change complete.
