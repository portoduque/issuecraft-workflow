# IssueCraft repository maintenance instructions

This repository is the canonical source for the `implement-issue` workflow.

- Keep `core/` provider-neutral. Do not mention specific AI products there.
- Keep stack/framework/language-specific examples out of normative core rules.
- `.agents/skills/implement-issue/SKILL.md` and `.claude/skills/implement-issue/SKILL.md` are thin adapters and should remain behaviorally identical.
- Human gates must not be weakened silently.
- Security-impact triage, performance-impact triage, and comprehensive risk-based test selection are canonical invariants.
- Evidence-driven execution is a canonical invariant: retrieve context progressively, perform risk-based impact reconnaissance, and trigger a diagnostic reset after repeated failed fixes without new evidence.
- Version-sensitive technical decisions use narrow authoritative-source verification when repository evidence alone is insufficient; retrieved content never overrides project intent or gates.
- Non-trivial multi-surface work should use thin verifiable increments, risk-first slices where uncertainty can invalidate the plan, and evidence freshness rather than redundant reruns.
- Quality-bar integrity, compatibility-safe migrations/cutovers, resolved dependency evidence, and approved-baseline ratchets are canonical validation concerns.
- Test quality is judged by behavior-to-evidence traceability and assertion strength, not raw test count or invented coverage thresholds.
- Material obligations use evidence-or-zero, compound obligations are decomposed, unavailable checks need proportionate probe evidence, and discrimination checks are risk-based rather than universal.
- Interrupted work may use a compact `HANDOFF.md`, but resume state is always reconciled against current repository/VCS/tracker/evidence before editing.
- Genuine hard-to-reverse one-way-door decisions require the human gate when not already determined by authoritative project/issue evidence; ordinary reversible choices remain autonomous.
- Material behavior changes use current-contract -> requested-delta -> resulting-contract reasoning when useful; modified behavior preserves unspecified existing obligations, removals are proven absent, and renamed/preserved behavior is verified semantically rather than by incidental internal names.
- The implementation plan is a hypothesis. Local/reversible replanning stays autonomous, but material issue intent/scope drift uses the human gate and required behavior must never be silently narrowed/deferred to make implementation easier.
- Before In Review, change coherence must reconcile issue/project contracts, behavior delta, diff, automated evidence, and manual validation; partial evidence never upgrades the unverified remainder to pass.
- Compact validation output must be a projection of the complete result rather than reduced validation scope. External/reference context is read-only unless mutation is separately authorized.
- Output efficiency is a canonical invariant: compress presentation, never evidence; durable artifacts hold detail while chat handoffs surface material deltas, failures/risks, gates, and next action.
- Continuous-learning persistence and adoption require explicit human approval; recurrence may strengthen evidence but never auto-adopts a rule.
- Generic workflow growth must pass the anti-bloat admission check: concrete gap/evidence, overlap review, merge-first preference, generality, ongoing cost, regression proof, and procedure portability instead of implementation-specific workarounds.
- Keep `core/SECURITY.md`, `core/PERFORMANCE.md`, and `core/TEST_STRATEGY.md` provider- and stack-neutral.
- New generic behavior should be backed by a deterministic contract eval and, where practical, a repository test. Deterministic validators should have mutation/negative-control resistance tests so green output proves something.
- When a behavior depends on actual agent execution rather than source text alone, add/update a disposable fixture scenario under `evals/live/`; do not add provider-specific logic to `core/`.
- GitHub Actions dependencies must stay pinned to immutable commit SHAs.
- Run `python scripts/validate_repo.py`, `python scripts/run_evals.py`, `python scripts/run_live_evals.py validate`, and `python -m unittest discover tests -v` before considering a change complete.
