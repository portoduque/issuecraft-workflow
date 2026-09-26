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
