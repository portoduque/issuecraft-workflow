# Changelog

All notable changes are documented here.

## 0.16.0 - 2026-09-27

Operational hardening release.

- Added managed IssueCraft state path-safety rules: all `.implement-issue/` writes stay inside the authorized repository, traversal is refused, redirecting symlink/junction/reparse-point paths are treated as unsafe, and issue keys are conservative single path segments with stable disambiguation when needed.
- Clarified that Profile/Blueprint/Rules/Learnings are project-scoped but not magically synchronized across isolated worktrees; optimistic concurrency applies only to state visible through the current workspace/integration point.
- Documented the two safe parallel-work distribution paths: install IssueCraft in each worktree that needs it, or use the project's approved/versioned runtime/adapters.
- Hardened first install so an existing same-name `implement-issue` adapter is not silently overwritten before an IssueCraft runtime exists; explicit `--overwrite-system` remains the intentional replacement/update path.
- Hardened release ZIP hygiene by excluding local live-eval runner config/results and generated coverage output in addition to existing VCS/cache exclusions.
- Strengthened the live `human-done-gate` scenario so real-agent evaluation requires the issue-scoped `.implement-issue/issues/ISSUE-001/MANUAL_VALIDATION_PLAN.md` path and rejects recreation of the legacy root-level plan.
- Updated architecture, project-file, installation, security, README, PR-template, contribution, and maintainer guidance for the v0.16 boundaries.
- Added deterministic scenarios 60-63 plus repository and validator-resistance tests for managed-state safety, worktree visibility, installer collisions, and release hygiene.
- Preserved the no-orchestrator design: no daemon, lock service, heartbeat, central state database, automatic worktree lifecycle, automatic rebase/merge, or provider-specific core logic was added.

## 0.15.0 - 2026-09-27

Parallel-work safety release.

- Added a lightweight parallel-work preflight: intentional concurrent mutation should prefer isolated physical workspaces/checkouts when available, while known concurrent mutation in the same physical working tree is treated as unsafe.
- Kept overlap advisory by default: isolated issues with disjoint surfaces continue concurrently; overlapping files/contracts increase integration risk but do not fabricate a dependency or execution order.
- Split project knowledge from issue execution state. `PROJECT_PROFILE`, `PROJECT_BLUEPRINT`, `PROJECT_RULES`, `LEARNINGS`, and proposals remain project-scoped, while handoff/manual-validation/execution-report artifacts now live under `.implement-issue/issues/<issue-key>/`.
- Added backward-compatible reads for unambiguous legacy root-level handoff/manual-validation artifacts without deleting ambiguous legacy state.
- Added optimistic concurrency for approved shared project-state writes: re-read current state before writing when concurrent modification is plausible, reconcile compatible changes, and treat material conflicts as stale approval under the existing approval-scope rule.
- Added integration-freshness validation before `In Review`: unrelated base movement preserves unaffected evidence, while materially relevant base changes invalidate and rerun only dependent checks.
- Added `docs/parallel-work.md` with an optional Git worktree example while keeping the canonical workflow VCS/provider/stack neutral.
- Deliberately did not add a daemon, lock server, database, heartbeat, agent registry, scheduler, file locks, automatic worktree creation, automatic rebase/merge, or direct agent-to-agent messaging.
- Added deterministic scenarios 56-59 plus repository and validator-resistance coverage.

## 0.14.0 - 2026-09-27

Quality and documentation integrity release.

- Added stack-neutral code-coverage discovery and policy: respect project tooling/thresholds/baselines, directly cover materially changed executable behavior when viable, and never lower/exclude/narrow coverage merely to make a change pass.
- Added canonical `coverage_policy` and `commands.coverage` fields to the Project Profile template/schema.
- Added IssueCraft-specific branch-aware Python code coverage using pinned `coverage==7.16.1` and a 90% CI gate without imposing that percentage on target projects.
- Simplified both READMEs from roughly 520 lines to roughly 260 lines while preserving clone/install/invoke/update/verification onboarding.
- Added an explicit eight-step human manual-validation procedure before `Done`.
- Moved advanced testing, validation, learning, and compatibility-release guidance into focused `docs/` pages.
- Corrected project-file documentation drift from `improvements/` to the canonical `proposals/` path.
- Added provider-neutral release smoke guidance for Codex, Claude Code, and Antigravity using disposable workspaces and the existing live-eval runner-adapter boundary.
- Added deterministic scenarios 53-55 plus repository/validator-resistance coverage for coverage policy, documentation integrity, and live-host compatibility claims.

## 0.13.0 - 2026-09-27

Project-language, deterministic-guardrail, and diagnostic-feedback release.

- Added project-language continuity: relevant project-owned glossary/ubiquitous-language/terminology sources are consumed on demand and treated as domain-language authority for new/changed material.
- Added pointer-over-copy guidance for persistent vocabulary references, with terminology conflicts surfaced instead of silently normalized and no automatic glossary creation or unrelated mass renames.
- Added deterministic-enforcement preference for mechanically decidable project rules when an existing proportionate project mechanism can enforce them.
- Kept judgement-bearing rules in human-readable project guidance and prohibited silently installing new tooling or expanding unrelated issue scope merely to automate a rule.
- Strengthened difficult/intermittent/performance diagnosis around the tightest feasible symptom-specific feedback signal before speculative fix loops.
- Preserved non-dogmatic testing: a faithful failing test remains preferred when practical, while traces, replayable artifacts, differential checks, measurements, and scoped instrumentation remain valid when they better represent the failure.
- Added deterministic scenarios 50-52 plus repository and validator-resistance coverage.
- Deliberately avoided mandatory TDD, user-approved test seams, automatic CONTEXT/glossary creation, multi-skill/router architecture, mandatory subagents, and deep-module design doctrine.

## 0.12.0 - 2026-09-27

Semantic-output-economy release.

- Strengthened compact communication with a semantic compression floor that preserves material negation/boundaries, identifiers, versions, values/units, states/statuses, commands/locations, failure identifiers, and explicit human decisions.
- Added a state-once rule so established material facts are repeated only when state changes, the current decision needs them, or omission would be ambiguous.
- Made progress updates information-bearing: routine tool mechanics are not narrated unless they carry a material finding, transition, failure, blocker, risk, gate, or correction.
- Added source-side narrowing/projection preference so targeted search/range/filter/field selection is preferred over retrieving large payloads only to summarize them afterward.
- Strengthened validation reporting for noisy logs/test output: surface decisive status/count/location/error evidence while preserving or referencing the complete diagnostic artifact.
- Added token-economy admission rules that require net-benefit evidence including recurring instruction/context overhead, extra turns/retries, and evidence/clarity effects.
- Added minimal-terse-control guidance for evaluating the marginal value of token-economy rules instead of crediting them for generic concision.
- Added deterministic scenarios 48-49 and regression coverage while deliberately avoiding caveman-style grammar, output caps, proxy/runtime compression, new modes/personas, or a new canonical core file.

## 0.11.0 - 2026-09-27

Approval-scope integrity release.

- Added a provider/stack-neutral approval-scope invariant: human authorization is bound to the material action/decision and target actually reviewed.
- Added pre-execution approval freshness checks for target/environment, material scope/effects, known risk, and gate-relevant preconditions.
- Material post-approval drift now invalidates stale authorization and requires the changed delta to be presented for fresh approval.
- Preserved autonomy for equivalent local/reversible implementation mechanics so the new invariant does not create approval ceremony.
- Clarified that authorization does not implicitly transfer across targets/environments or to materially distinct rollback, recovery, cleanup, destructive correction, or production-impacting follow-up work.
- Added deterministic scenario 47 plus repository and validator-resistance coverage for the new contract.
- Deliberately avoided plan digests, cross-artifact hash graphs, new schemas, persistent approval artifacts, or a new canonical core file.

## 0.10.0 - 2026-09-27

Solution-economy and evaluation-rigor release.

- Added a provider/stack-neutral solution-economy ladder: no new implementation when unnecessary -> existing project capability -> runtime/platform capability -> already-approved dependency -> smallest coherent new implementation.
- Defined solution economy as reducing justified ownership/complexity, not raw LOC, file count, deletion count, cleverness, token count, or dependency count.
- Added evidence-backed root-cause placement: bug fixes prefer the smallest common correct enforcement point when sibling paths share the same invariant, with broader validation for broader shared surfaces.
- Added a proof floor before simplicity: correctness/completeness and applicable security, accessibility, compatibility, preservation, data-integrity, reliability, and validation obligations cannot be traded for implementation economy.
- Added a solution-economy/ownership review before In Review for speculative abstractions, wrappers, dependencies, configuration, duplicated project capability, and unjustified future-proofing.
- Added durable reporting for material known operational ceilings and evidence-based revisit triggers without introducing a source-code debt marker or new ledger.
- Added provider-neutral delegation constraint continuity: delegation is optional, inherited constraints are never assumed, delegates cannot approve human gates, and the controlling workflow remains responsible for reconciliation/validation.
- Strengthened continuous-improvement admission so null/negative eval results are valid evidence for non-adoption rather than a reason to keep adding prompt text.
- Hardened live-agent comparison methodology: blind baseline/candidate pairing now requires verified runner isolation evidence to reduce intervention contamination risk.
- Added calibration guidance for future automated live-eval scorers/judges using known-good positive and known-bad negative controls when practical.
- Added a live root-cause-shared-path fixture and expanded deterministic contract coverage from 40 to 46 scenarios.
- Extended repository tests and validator mutation-resistance coverage for the v0.10 contracts.
- Preserved the anti-bloat boundary: no always-on hooks, modes/personas, LOC scoring, platform-native catalog, debt-comment convention, new canonical core file, mandatory subagent, or new runtime dependency.

## 0.9.0 - 2026-09-27

Behavior-delta, preservation, and change-coherence release.

- Added current-contract -> requested-delta -> resulting-contract reasoning for material behavior changes without introducing persistent spec files or an artifact-graph runtime.
- Added semantic handling for added, modified, removed, renamed/preserved, and unchanged-but-at-risk behavior.
- Added preservation obligations so modifying one contract member cannot silently drop existing scenarios, fields, states, roles, error paths, or compatibility behavior that the issue did not supersede.
- Added scope integrity: required behavior cannot be silently narrowed, deferred, waived, or redefined merely because implementation is harder than expected.
- Added material issue intent/scope drift gating while preserving autonomous local/reversible replanning for the same accepted outcome.
- Added change-coherence review across issue/acceptance criteria, project contracts, behavior delta, implementation diff, automated evidence, and manual validation.
- Added material-diff justification traceability and actionable evidence-backed findings.
- Added partial-evidence semantics: proven subsets remain useful but never upgrade unverified material members to a full pass.
- Clarified that compact output is a projection of the complete validation result, never reduced validation scope.
- Added mutable-authority rereads at resume/material phase transitions and the rule that reference/read scope does not grant mutation authority.
- Added proportional planning rigor and active-change overlap as advisory coordination risk unless an explicit/evidenced dependency establishes ordering.
- Added observable-behavior-over-implementation-detail testing guidance and regression protection against silent scenario/obligation loss.
- Expanded deterministic contract coverage from 33 to 40 scenarios and extended validator mutation-resistance coverage.
- Added one optional provider-neutral live-agent fixture for modified-contract preservation.
- Preserved provider/stack neutrality and deliberately did not add persistent specs, custom workflow schemas, artifact DAGs, archive machinery, mandatory planning pauses, or a multi-repository orchestration engine.

## 0.8.0 - 2026-09-27

Evidence-strength and resumability release.

- Added evidence-or-zero semantics so a material obligation is not considered covered without concrete proof of the required outcome.
- Added compound-obligation decomposition for independently falsifiable fields, clauses, states, roles, cases, and enumerated members.
- Added verification-precision gaps so vague requirements remain explicitly unproven instead of receiving invented thresholds or exact outcomes.
- Added risk-based isolated discrimination/fault checks for high-risk or uncertain test oracles without making mutation testing mandatory.
- Added probe-before-unavailable semantics: applicable checks require proportionate safe evidence before being labeled unavailable.
- Added compact resumable `.implement-issue/HANDOFF.md` state for interrupted/incomplete work, with mandatory reconciliation against current repository/VCS/tracker/evidence before edits.
- Added a human gate for genuine hard-to-reverse one-way-door implementation decisions while keeping ordinary reversible engineering autonomous.
- Clarified that recurring independent observations strengthen improvement evidence but never auto-promote a learning into persistent or normative behavior.
- Expanded deterministic contract coverage from 28 to 33 scenarios.
- Added maintainer-only validator resistance testing that mutates a clean repository copy, requires the validator to kill broken invariants, and includes a harmless negative control.
- Preserved provider/stack neutrality and added no runtime dependency, mandatory subagent, mandatory TDD rule, universal mutation count, or auto-learning engine.

## 0.7.0 - 2026-09-27

Source-verification, incremental execution, and quality-bar hardening release.

- Added version-aware authoritative-source verification for material version-sensitive technical decisions, with narrow retrieval, untrusted-content handling, and explicit unverified states.
- Added thin independently verifiable implementation increments and risk-first slices for plan-invalidating uncertainty without forcing artificial slicing on trivial changes.
- Added validation cadence and evidence-freshness semantics so focused checks run near the change, stale evidence is rerun, and unchanged green checks are not repeated merely for reassurance.
- Added quality-bar integrity review for weakened thresholds, removed checks, weakened tests, suppressions/bypasses, unfinished stubs, and silent-failure paths.
- Added compatibility-safe expand -> migrate/cut over -> contract guidance for coexistence-sensitive migrations, while requiring truthful recovery semantics instead of invented rollback claims.
- Strengthened dependency/toolchain change review with resolved lock-state, authoritative release/migration evidence, transitive effects, and contract-focused tests.
- Added baseline ratchets only when project evidence makes the baseline normative; no incidental metric becomes policy and no universal tolerance is invented.
- Strengthened anti-bloat governance so implementation-specific workarounds stay out of canonical core until a provider-neutral engineering need is demonstrated.
- Expanded deterministic contract coverage from 21 to 28 scenarios.
- Added a live deadline-pressure scenario that checks evidence honesty, quality-bar integrity, and the human-owned Done gate.
- Preserved provider/stack neutrality and added no runtime dependency, persona, hook, mandatory TDD rule, or universal numeric quality threshold.

## 0.6.0 - 2026-09-27

Evidence-driven execution and test-quality release.

- Added progressive issue-context retrieval with explicit stopping criteria to reduce unnecessary repository/context expansion.
- Added risk-based impact reconnaissance for materially coupled changes without forcing call-graph work on trivial edits.
- Added a diagnostic-reset protocol for repeated failed fixes without new evidence: recapture failure, verify actual state, restate evidence-backed hypothesis, shrink scope, run a discriminating diagnostic, then revise before editing.
- Added behavior/acceptance-criterion to verification-evidence traceability.
- Added lowest-sufficient test-fidelity selection so expensive integration/system/E2E checks are used only when lower layers cannot faithfully prove the behavior.
- Strengthened test-oracle quality: assertions must materially discriminate correct behavior from the relevant regression.
- Tightened bug-fix RED semantics so unrelated setup/environment/pre-existing failures do not count as a valid reproducer.
- Added path-parity and sibling-surface regression checks when one root cause can affect equivalent execution paths.
- Added contract-preserving guidance for mocks/fakes/stubs, instrumented runtime diagnostics, risk-prioritized E2E, and useful failure-artifact preservation.
- Added evidence-backed diff review where zero findings is explicitly valid and severity must be supported.
- Added an anti-bloat generic-change admission check so popularity/novelty cannot justify append-only workflow growth.
- Added deterministic scenarios 18-21 plus a live diagnostic-reset fixture.
- Preserved provider/stack neutrality and avoided new runtime dependencies, hooks, agents, arbitrary coverage thresholds, or mandatory TDD.


## 0.5.0 - 2026-09-27

Output-efficiency release.

- Added a canonical communication contract: analyze deeply, report minimally, and compress presentation without losing evidence.
- Made durable artifacts the detailed source of truth while chat handoffs focus on material deltas, decisions, blockers, risks, and next action.
- Added delta-only progress guidance to avoid repeatedly restating unchanged project/workflow state.
- Added compact grouping for routine passes and not-applicable validation while keeping failures, unavailable checks, residual risks, and human gates explicit.
- Prevented generated manual-validation and other durable artifacts from being duplicated in full in normal chat handoffs.
- Kept non-blocking secondary findings separate from the active issue to reduce tangents and scope creep.
- Added deterministic contract regression coverage for output efficiency (scenario 17).
- Extended live-agent evaluation guidance with communication-efficiency review and token/cost comparison as a secondary metric only after quality/safety requirements are met.


## 0.4.0 - 2026-09-27

Live-agent evaluation release.

- Added an optional provider-neutral live-agent evaluation harness outside the installed workflow runtime.
- Added disposable fixture repositories so real-agent tests never need to run against production or personal projects.
- Added multi-turn live scenarios for the human-owned Done gate and continuous-learning persistence gate.
- Added baseline vs candidate runs using the same scenario/fixture, with IssueCraft installed only for the candidate condition.
- Added transcript plus workspace-diff capture so behavioral evaluation can inspect what the agent actually changed.
- Added deterministic blind A/B export with the condition mapping stored separately.
- Added a neutral runner-adapter protocol instead of embedding provider-specific CLIs into the core.
- Added a qualitative rubric focused on correctness, evidence fidelity, safety/human gates, validation quality, scope discipline, and autonomy without premature synthetic weights.
- Added deterministic repository tests for live scenario validation, disposable execution, baseline/candidate isolation, duplicate-run protection, multi-turn capability declarations, and blind pairing.
- Kept real host compatibility smoke tests optional and outside canonical CI to avoid external CLI/auth/network instability in the core release gate.

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
