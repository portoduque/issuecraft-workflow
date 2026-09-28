#!/usr/bin/env python3
"""Deterministic, provider-neutral contract evals for IssueCraft.

These assertions do not pretend to measure a live model. They verify that each
human-readable eval scenario has an executable repository-level invariant.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
SCENARIOS = ROOT / "evals" / "scenarios"

VENDOR_TERMS = re.compile(r"\b(codex|claude|antigravity|openai|anthropic|gemini)\b", re.I)
STACK_TERMS = re.compile(
    r"\b(typescript|javascript|python|java|kotlin|swift|rust|react|django|fastapi|spring|"
    r"postgresql|mysql|mongodb|redis|npm|pnpm|yarn|pytest|jest|vitest|flyway|liquibase|prisma)\b",
    re.I,
)

EXPECTED_SCENARIOS = [
    "01-existing-project.md",
    "02-empty-project.md",
    "03-documented-empty.md",
    "04-drift.md",
    "05-unknown-not-invented.md",
    "06-human-done-gate.md",
    "07-no-tracker-write.md",
    "08-monorepo.md",
    "09-preserve-user-changes.md",
    "10-improvement-proposal.md",
    "11-security-sensitive.md",
    "12-performance-sensitive.md",
    "13-test-taxonomy.md",
    "14-agent-neutrality.md",
    "15-stack-neutrality.md",
    "16-safe-expensive-tests.md",
    "17-output-efficiency.md",
    "18-diagnostic-reset.md",
    "19-progressive-context-impact.md",
    "20-test-evidence-quality.md",
    "21-generic-change-admission.md",
    "22-version-aware-source-verification.md",
    "23-incremental-evidence-freshness.md",
    "24-quality-bar-integrity.md",
    "25-compatible-migrations.md",
    "26-dependency-change-evidence.md",
    "27-approved-baseline-ratchet.md",
    "28-procedure-not-workaround.md",
    "29-evidence-or-zero-compound.md",
    "30-probe-before-unavailable.md",
    "31-risk-based-discrimination.md",
    "32-resumable-handoff.md",
    "33-one-way-door-gate.md",
    "34-behavior-delta-semantics.md",
    "35-modified-preservation.md",
    "36-intent-scope-integrity.md",
    "37-change-coherence-review.md",
    "38-partial-evidence-projection.md",
    "39-mutable-authority-reference-scope.md",
    "40-progressive-planning-overlap.md",
    "41-solution-economy.md",
    "42-root-cause-placement.md",
    "43-proof-floor-before-economy.md",
    "44-solution-economy-review.md",
    "45-delegation-constraint-continuity.md",
    "46-live-eval-methodology.md",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def require(text: str, *phrases: str) -> None:
    lowered = text.lower()
    for phrase in phrases:
        if phrase.lower() not in lowered:
            raise AssertionError(f"missing contract phrase: {phrase}")


def eval_existing_project() -> None:
    require(read("core/PROJECT_DISCOVERY.md"), "Proposed Profile", "explicit human approval", "evidence")


def eval_empty_project() -> None:
    require(read("core/PROJECT_BOOTSTRAP.md"), "Empty/near-empty", "PROJECT_BLUEPRINT", "undecided")


def eval_documented_empty() -> None:
    require(read("core/PROJECT_BOOTSTRAP.md"), "Read meaningful project docs/specs/ADRs first", "Ask questions only")


def eval_drift() -> None:
    text = read("core/DRIFT_DETECTION.md")
    require(text, "Do not edit the Profile automatically", "security tooling", "performance tooling", "observability")


def eval_unknown_not_invented() -> None:
    require(read("core/WORKFLOW.md"), "Never fabricate")
    require(read("core/PROJECT_DISCOVERY.md"), "unknown", "Do not infer")


def eval_human_done_gate() -> None:
    require(read("core/HUMAN_GATES.md"), "Only a human can satisfy final manual validation")


def eval_no_tracker_write() -> None:
    require(read("core/CAPABILITIES.md"), "no `tracker.write`", "report the intended state transition")


def eval_monorepo() -> None:
    require(read("core/PROJECT_DISCOVERY.md"), "monorepo", "Do not assume one global stack")


def eval_preserve_user_changes() -> None:
    require(read("core/WORKFLOW.md"), "Preserve unrelated user changes")


def eval_improvement_proposal() -> None:
    text = read("core/CONTINUOUS_IMPROVEMENT.md")
    require(
        text,
        "must not self-modify silently",
        ".implement-issue/proposals/",
        ".implement-issue/LEARNINGS.md",
        "explicit human approval",
        "Recurrence strengthens evidence, not authority",
        "Recurrence never auto-promotes",
    )
    require(read("core/HUMAN_GATES.md"), "Persistence and adoption are distinct decisions")


def eval_security_sensitive() -> None:
    text = read("core/SECURITY.md")
    require(text, "security-impact triage", "material security regression", "blocks `In Review`")


def eval_performance_sensitive() -> None:
    text = read("core/PERFORMANCE.md")
    require(text, "performance-impact triage", "performance budget", "blocks `In Review`")


def eval_test_taxonomy() -> None:
    text = read("core/TEST_STRATEGY.md").lower()
    for phrase in ("unit", "integration", "contract", "end-to-end", "regression", "property-based", "fuzz", "mutation", "concurrency", "accessibility", "load", "stress", "soak", "migration"):
        if phrase not in text:
            raise AssertionError(f"missing test family: {phrase}")


def eval_agent_neutrality() -> None:
    for path in CORE.glob("*.md"):
        match = VENDOR_TERMS.search(path.read_text(encoding="utf-8"))
        if match:
            raise AssertionError(f"provider term leaked into core: {path.name}: {match.group(0)}")


def eval_stack_neutrality() -> None:
    for path in CORE.glob("*.md"):
        match = STACK_TERMS.search(path.read_text(encoding="utf-8"))
        if match:
            raise AssertionError(f"stack term leaked into core: {path.name}: {match.group(0)}")


def eval_safe_expensive_tests() -> None:
    require(read("core/PERFORMANCE.md"), "Do not run destructive or high-load tests against production/shared systems without explicit authorization")
    require(read("core/CAPABILITIES.md"), "High-load, destructive, production-impacting")


def eval_output_efficiency() -> None:
    workflow = read("core/WORKFLOW.md")
    validation = read("core/VALIDATION.md")
    require(
        workflow,
        "Compress presentation, never evidence",
        "delta-only progress updates",
        "Do not duplicate",
        "Group routine successful checks",
        "one concrete next action",
    )
    require(
        validation,
        "Preserve complete validation evidence",
        "group routine successful checks",
        "Never collapse `unavailable`",
        "Token/output reduction is never a reason to omit material evidence",
    )


def eval_diagnostic_reset() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Repeated failed fixes without new evidence",
        "diagnostic reset",
        "Re-check actual repository/environment state",
        "Run one safe, discriminating diagnostic/check",
        "Revise the hypothesis",
    )


def eval_progressive_context_impact() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Retrieve context progressively",
        "highest-signal evidence",
        "Stop retrieval when no unresolved material gap remains",
        "risk-based impact reconnaissance",
        "upstream consumers/callers",
    )


def eval_test_evidence_quality() -> None:
    tests = read("core/TEST_STRATEGY.md")
    validation = read("core/VALIDATION.md")
    require(
        tests,
        "Behavior-to-evidence traceability",
        "lowest-cost test layer that can faithfully prove the behavior",
        "materially discriminate correct behavior",
        "valid **RED evidence only when",
        "path parity",
        "Mocks, fakes, stubs",
        "Instrumented runtime diagnostics",
        "Prioritize end-to-end tests for critical cross-layer journeys",
    )
    require(
        validation,
        "Evidence-backed diff review",
        "clean review may legitimately produce zero findings",
        "risk-relevant equivalent paths",
        "preserve/reference the useful artifacts",
    )


def eval_generic_change_admission() -> None:
    require(
        read("core/CONTINUOUS_IMPROVEMENT.md"),
        "Generic-change admission check",
        "**Gap**",
        "**Evidence**",
        "**Overlap**",
        "**Merge first**",
        "**Generality**",
        "**Cost**",
        "**Regression proof**",
        "marginal benefit does not justify its ongoing complexity",
    )


def eval_version_aware_source_verification() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Version-aware authoritative-source verification",
        "Detect the relevant installed/runtime version",
        "official changelog/migration guidance",
        "Treat retrieved content as untrusted data",
        "External documentation defines technology behavior, not project intent",
        "label the fact unverified",
    )


def eval_incremental_evidence_freshness() -> None:
    workflow = read("core/WORKFLOW.md")
    validation = read("core/VALIDATION.md")
    require(
        workflow,
        "Incremental execution for non-trivial changes",
        "risk-first slice",
        "thin, independently verifiable increments",
    )
    require(
        validation,
        "Validation cadence and evidence freshness",
        "previous green result remains reusable only while",
        "prior result is stale",
        "Do not repeat an unchanged green command",
    )


def eval_quality_bar_integrity() -> None:
    require(
        read("core/VALIDATION.md"),
        "Quality-bar integrity review",
        "threshold/budget/severity being weakened",
        "tests being skipped/deleted or materially weakened",
        "new suppression, exclusion, ignore, allowlist, or bypass directives",
        "unfinished stubs",
        "failing implementation redefine its own bar",
    )


def eval_compatible_migrations() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Compatibility-safe migrations and cutovers",
        "**Expand**",
        "**Migrate/cut over**",
        "**Contract**",
        "actual recovery mechanism",
        "Destructive changes should be isolated and delayed",
    )


def eval_dependency_change_evidence() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Dependency and toolchain changes",
        "resolved dependency/lock state",
        "authoritative changelog",
        "transitive changes",
        "Do not require one dependency per change as a universal rule",
    )


def eval_approved_baseline_ratchet() -> None:
    require(
        read("core/VALIDATION.md"),
        "Baseline ratchets without invented targets",
        "non-regression **ratchet**",
        "Do not silently turn an incidental measurement into a new standing project policy",
        "never invent a universal tolerance",
    )


def eval_procedure_not_workaround() -> None:
    require(
        read("core/CONTINUOUS_IMPROVEMENT.md"),
        "**Procedure portability**",
        "generic engineering procedure",
        "presume the change belongs in an adapter",
        "could the rule still be justified without naming the model/host/tool",
    )


def eval_evidence_or_zero_compound() -> None:
    tests = read("core/TEST_STRATEGY.md")
    validation = read("core/VALIDATION.md")
    require(
        tests,
        "Evidence-or-zero",
        "Compound obligation decomposition",
        "Verification precision gaps",
        "Related tests exist",
        "unproven/unverified",
    )
    require(
        validation,
        "evidence-or-zero",
        "decompose compound/enumerated requirements",
        "verification precision gaps",
    )


def eval_probe_before_unavailable() -> None:
    require(
        read("core/VALIDATION.md"),
        "Probe before `unavailable`",
        "safe execution attempt",
        "safe prerequisite/capability probe",
        "narrative assumption",
        "Do not perform a destructive",
    )


def eval_risk_based_discrimination() -> None:
    require(
        read("core/TEST_STRATEGY.md"),
        "Risk-based discrimination checks",
        "isolated disposable state",
        "surviving fault",
        "do not require mutation/fault injection for every issue",
        "universal number of mutations",
    )


def eval_resumable_handoff() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Session handoff and resume",
        ".implement-issue/HANDOFF.md",
        "resume hypothesis",
        "Reconcile it against current repository/VCS state",
        "current evidence win over stale narrative",
        "Replace or clear the handoff",
    )


def eval_one_way_door_gate() -> None:
    require(
        read("core/HUMAN_GATES.md"),
        "Gate G — hard-to-reverse implementation decisions",
        "explicit human decision",
        "genuine one-way doors",
        "ordinary local implementation choices",
    )


def eval_behavior_delta_semantics() -> None:
    workflow = read("core/WORKFLOW.md")
    tests = read("core/TEST_STRATEGY.md")
    require(
        workflow,
        "behavior delta model",
        "current contract -> requested delta -> intended resulting contract",
        "added",
        "modified",
        "removed",
        "renamed/preserved",
        "unchanged-but-at-risk",
        "current contract",
        "requested delta",
        "resulting contract",
    )
    require(
        tests,
        "Behavior-delta test semantics",
        "observable behavior/contract",
        "removed behavior is absent/inaccessible",
        "renamed/preserved",
    )


def eval_modified_preservation() -> None:
    workflow = read("core/WORKFLOW.md")
    tests = read("core/TEST_STRATEGY.md")
    validation = read("core/VALIDATION.md")
    require(
        workflow,
        "preservation obligations",
        "A modification is not permission to drop unspecified behavior",
    )
    require(
        tests,
        "scenario/obligation loss is a regression",
        "silently dropping the unchanged cases",
    )
    require(
        validation,
        "preservation obligations remain intact",
        "do not let a partial rewrite silently erase",
        "baseline cannot be established",
    )


def eval_intent_scope_integrity() -> None:
    workflow = read("core/WORKFLOW.md")
    lifecycle = read("core/ISSUE_LIFECYCLE.md")
    gates = read("core/HUMAN_GATES.md")
    require(
        workflow,
        "implementation plan is a working hypothesis",
        "issue intent/scope drift",
        "Preserve **scope integrity**",
        "do not silently narrow, defer, waive, or redefine",
    )
    require(lifecycle, "intent and scope identity", "replan autonomously")
    require(
        gates,
        "Gate H — material issue intent/scope drift",
        "core problem",
        "externally observable outcome",
        "Do **not** gate ordinary replanning",
    )


def eval_change_coherence_review() -> None:
    require(
        read("core/VALIDATION.md"),
        "Change coherence review",
        "material diff change needs justification traceability",
        "issue intent and acceptance criteria",
        "implementation diff",
        "automated test/validation evidence",
        "manual validation plan",
        "specific corrective action when the evidence makes one known",
    )


def eval_partial_evidence_projection() -> None:
    evidence = read("core/EVIDENCE_MODEL.md")
    validation = read("core/VALIDATION.md")
    require(
        evidence,
        "Partial evidence",
        "does not prove the unobserved members",
        "unsupported remainder unverified/unknown",
        "no contradictory evidence found",
    )
    require(
        validation,
        "Partial evidence is not full verification",
        "only four are proven, report four proven and two unverified",
        "overall `pass` requires evidence for every material applicable member",
        "Compact output must be a projection of the complete validation result",
        "never a reduced validation scope",
    )


def eval_mutable_authority_reference_scope() -> None:
    workflow = read("core/WORKFLOW.md")
    evidence = read("core/EVIDENCE_MODEL.md")
    require(
        workflow,
        "mutable authoritative inputs",
        "instead of relying on conversation memory",
        "Reference scope is not mutation scope",
        "does not authorize modifying it",
    )
    require(
        evidence,
        "Mutable evidence and conversation memory",
        "is not a substitute for the current authoritative source",
        "re-read the specific live issue/project/rule/configuration/code/validation inputs",
    )


def eval_progressive_planning_overlap() -> None:
    workflow = read("core/WORKFLOW.md")
    lifecycle = read("core/ISSUE_LIFECYCLE.md")
    require(
        workflow,
        "Scale planning depth to risk and ambiguity",
        "trivial local reversible edit needs no artificial ceremony",
        "public-contract, data, security, migration, cross-surface",
        "active change touching the same public contract",
        "Overlap alone is not an implicit dependency",
    )
    require(
        lifecycle,
        "coordination risk",
        "Do not infer a dependency or execution order",
    )


def eval_solution_economy() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Solution economy and root-cause placement",
        "No new implementation",
        "Existing project capability",
        "Runtime/platform capability",
        "Already-approved dependency",
        "ownership and justified complexity",
        "not raw line count, file count",
        "speculative abstractions",
    )


def eval_root_cause_placement() -> None:
    require(
        read("core/WORKFLOW.md"),
        "smallest common correct enforcement point",
        "callers/sibling paths",
        "shared cause",
        "broadens blast radius",
        "broader contract",
    )


def eval_proof_floor_before_economy() -> None:
    require(
        read("core/TEST_STRATEGY.md"),
        "Proof floor before solution economy",
        "correctness/completeness",
        "proof obligations, not bloat metrics",
        "Fewer lines, files, dependencies, abstractions, turns, tokens, or lower cost never compensate",
        "same required proof floor",
    )


def eval_solution_economy_review() -> None:
    validation = read("core/VALIDATION.md")
    report = read("templates/ISSUE_EXECUTION_REPORT.md")
    require(
        validation,
        "Solution-economy / ownership review",
        "avoid avoidable ownership or speculative complexity",
        "Do **not** use raw LOC, file count, deletion count, or dependency count as quality scores",
        "material known operational ceiling",
        "evidence-based revisit trigger",
    )
    require(
        report,
        "Solution economy / known limits",
        "Known operational ceiling",
        "Evidence-based revisit trigger",
    )


def eval_delegation_constraint_continuity() -> None:
    require(
        read("core/WORKFLOW.md"),
        "Delegation constraint continuity",
        "Delegation is optional",
        "do not assume project rules, issue intent, human gates",
        "cannot approve a human gate",
        "parent/controlling workflow remains responsible",
        "delegation must not become a way to bypass",
    )


def eval_live_eval_methodology() -> None:
    live = read("evals/live/README.md")
    rubric = read("evals/live/rubric.md")
    learning = read("core/CONTINUOUS_IMPROVEMENT.md")
    runner = read("scripts/run_live_evals.py")
    require(
        live,
        "intervention isolation is verified",
        "Blind pairing refuses",
        "Evaluation instrument calibration",
        "known-good/positive control",
        "known-bad/negative control",
        "Null and negative results",
    )
    require(
        runner,
        "verified runner isolation evidence",
        "verified isolation requires concrete evidence",
    )
    require(
        rubric,
        "Solution economy",
        "tie/null result is legitimate",
        "irrelevant when it comes from missing behavior",
    )
    require(
        learning,
        "Failure to demonstrate benefit is valid evidence for non-adoption",
        "null result",
    )


EVALS = [
    eval_existing_project,
    eval_empty_project,
    eval_documented_empty,
    eval_drift,
    eval_unknown_not_invented,
    eval_human_done_gate,
    eval_no_tracker_write,
    eval_monorepo,
    eval_preserve_user_changes,
    eval_improvement_proposal,
    eval_security_sensitive,
    eval_performance_sensitive,
    eval_test_taxonomy,
    eval_agent_neutrality,
    eval_stack_neutrality,
    eval_safe_expensive_tests,
    eval_output_efficiency,
    eval_diagnostic_reset,
    eval_progressive_context_impact,
    eval_test_evidence_quality,
    eval_generic_change_admission,
    eval_version_aware_source_verification,
    eval_incremental_evidence_freshness,
    eval_quality_bar_integrity,
    eval_compatible_migrations,
    eval_dependency_change_evidence,
    eval_approved_baseline_ratchet,
    eval_procedure_not_workaround,
    eval_evidence_or_zero_compound,
    eval_probe_before_unavailable,
    eval_risk_based_discrimination,
    eval_resumable_handoff,
    eval_one_way_door_gate,
    eval_behavior_delta_semantics,
    eval_modified_preservation,
    eval_intent_scope_integrity,
    eval_change_coherence_review,
    eval_partial_evidence_projection,
    eval_mutable_authority_reference_scope,
    eval_progressive_planning_overlap,
    eval_solution_economy,
    eval_root_cause_placement,
    eval_proof_floor_before_economy,
    eval_solution_economy_review,
    eval_delegation_constraint_continuity,
    eval_live_eval_methodology,
]


def run() -> list[str]:
    errors: list[str] = []
    actual = sorted(path.name for path in SCENARIOS.glob("*.md"))
    if actual != EXPECTED_SCENARIOS:
        errors.append(f"scenario set mismatch: expected {EXPECTED_SCENARIOS}, got {actual}")
        return errors

    for scenario, check in zip(EXPECTED_SCENARIOS, EVALS):
        try:
            check()
        except Exception as exc:
            errors.append(f"{scenario}: {exc}")
    return errors


def main() -> int:
    errors = run()
    if errors:
        print("CONTRACT EVALS FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"CONTRACT EVALS PASSED ({len(EVALS)}/{len(EVALS)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
