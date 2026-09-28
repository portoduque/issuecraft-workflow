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
    require(text, "must not self-modify silently", ".implement-issue/proposals/", ".implement-issue/LEARNINGS.md", "explicit human approval")
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
