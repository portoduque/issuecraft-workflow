# Repository maintenance instructions

This repository is the canonical source for the `implement-issue` workflow.

- Keep `core/` provider-neutral. Do not mention specific AI products there.
- Keep stack/framework/language-specific examples out of normative core rules.
- `.agents/skills/implement-issue/SKILL.md` and `.claude/skills/implement-issue/SKILL.md` are thin adapters and should remain behaviorally identical.
- Human gates must not be weakened silently.
- Security-impact triage, performance-impact triage, and comprehensive risk-based test selection are canonical invariants.
- Keep `core/SECURITY.md`, `core/PERFORMANCE.md`, and `core/TEST_STRATEGY.md` provider- and stack-neutral.
- New generic behavior should be backed by an eval scenario.
- Run `python scripts/validate_repo.py` and `python -m unittest discover tests -v` before considering a change complete.
