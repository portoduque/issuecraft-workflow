#!/usr/bin/env python3
"""Structural and security checks for the IssueCraft workflow source repository."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "VERSION",
    "manifest.json",
    "README.md",
    "README.pt-BR.md",
    "core/WORKFLOW.md",
    "core/CAPABILITIES.md",
    "core/EVIDENCE_MODEL.md",
    "core/PROJECT_DISCOVERY.md",
    "core/PROJECT_BOOTSTRAP.md",
    "core/DRIFT_DETECTION.md",
    "core/HUMAN_GATES.md",
    "core/ISSUE_LIFECYCLE.md",
    "core/VALIDATION.md",
    "core/TEST_STRATEGY.md",
    "core/SECURITY.md",
    "core/PERFORMANCE.md",
    "core/CONTINUOUS_IMPROVEMENT.md",
    "schemas/project-profile.schema.json",
    "schemas/project-blueprint.schema.json",
    "templates/PROJECT_PROFILE.yaml",
    "templates/PROJECT_BLUEPRINT.yaml",
    "templates/LEARNINGS.md",
    "templates/WORKFLOW_IMPROVEMENT_PROPOSAL.md",
    "templates/HANDOFF.md",
    ".agents/skills/implement-issue/SKILL.md",
    ".claude/skills/implement-issue/SKILL.md",
    "scripts/run_evals.py",
    "scripts/run_live_evals.py",
    "evals/live/README.md",
    "evals/live/rubric.md",
    "evals/live/runners.example.json",
    "tests/test_validator_resistance.py",
]
VENDOR_TERMS = re.compile(r"\b(codex|claude|antigravity|openai|anthropic|gemini)\b", re.I)
STACK_TERMS = re.compile(
    r"\b(typescript|javascript|python|java|kotlin|swift|rust|react|django|fastapi|spring|"
    r"postgresql|mysql|mongodb|redis|npm|pnpm|yarn|pytest|jest|vitest|flyway|liquibase|prisma)\b",
    re.I,
)
ACTION_REF = re.compile(r"^\s*uses:\s*[^@\s]+@([0-9a-f]{40})(?:\s+#.*)?$", re.M)


def check_required(errors: list[str]) -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")


def check_json(errors: list[str]) -> None:
    for path in list((ROOT / "schemas").glob("*.json")) + [ROOT / "manifest.json"]:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


def check_skills(errors: list[str]) -> None:
    paths = [
        ROOT / ".agents/skills/implement-issue/SKILL.md",
        ROOT / ".claude/skills/implement-issue/SKILL.md",
    ]
    texts: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        texts.append(text)
        fm = parse_frontmatter(text)
        if fm.get("name") != "implement-issue":
            errors.append(f"invalid/missing skill name in {path.relative_to(ROOT)}")
        if not fm.get("description"):
            errors.append(f"missing skill description in {path.relative_to(ROOT)}")
        if "core/WORKFLOW.md" not in text:
            errors.append(f"adapter does not delegate to canonical workflow: {path.relative_to(ROOT)}")
    if len(set(texts)) != 1:
        errors.append("agent skill adapters must be behaviorally identical")


def check_core_neutrality(errors: list[str]) -> None:
    for path in (ROOT / "core").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        vendor = VENDOR_TERMS.search(text)
        if vendor:
            errors.append(f"provider term '{vendor.group(0)}' leaked into canonical core: {path.relative_to(ROOT)}")
        stack = STACK_TERMS.search(text)
        if stack:
            errors.append(f"stack-specific term '{stack.group(0)}' leaked into canonical core: {path.relative_to(ROOT)}")


def check_quality_contracts(errors: list[str]) -> None:
    workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
    validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
    tests = (ROOT / "core/TEST_STRATEGY.md").read_text(encoding="utf-8")
    security = (ROOT / "core/SECURITY.md").read_text(encoding="utf-8")
    performance = (ROOT / "core/PERFORMANCE.md").read_text(encoding="utf-8")
    for phrase in ("TEST_STRATEGY.md", "SECURITY.md", "PERFORMANCE.md", "security-impact triage", "performance-impact triage"):
        if phrase not in workflow:
            errors.append(f"workflow quality contract missing phrase: {phrase}")
    for phrase in ("Unit", "Integration", "Contract", "End-to-end", "Regression", "property-based", "fuzz", "mutation", "concurrency", "accessibility", "load", "stress", "soak", "compatibility", "migration"):
        if phrase.lower() not in tests.lower():
            errors.append(f"test taxonomy missing category: {phrase}")
    if "material security regression" not in security:
        errors.append("security blocker contract missing")
    if "performance budget" not in performance:
        errors.append("performance budget contract missing")
    if "not_applicable" not in validation or "unavailable" not in validation:
        errors.append("validation must distinguish not_applicable from unavailable")
    for phrase in ("Compress presentation, never evidence", "delta-only progress updates", "Group routine successful checks"):
        if phrase not in workflow:
            errors.append(f"output efficiency contract missing phrase: {phrase}")
    for phrase in ("Preserve complete validation evidence", "Token/output reduction is never a reason to omit material evidence"):
        if phrase not in validation:
            errors.append(f"validation output-efficiency contract missing phrase: {phrase}")
    for phrase in ("diagnostic reset", "Retrieve context progressively", "risk-based impact reconnaissance"):
        if phrase.lower() not in workflow.lower():
            errors.append(f"workflow evidence-efficiency contract missing phrase: {phrase}")
    for phrase in (
        "Behavior-to-evidence traceability",
        "lowest-cost test layer that can faithfully prove the behavior",
        "path parity",
        "Mocks, fakes, stubs",
        "Instrumented runtime diagnostics",
    ):
        if phrase.lower() not in tests.lower():
            errors.append(f"test evidence-quality contract missing phrase: {phrase}")
    for phrase in ("Evidence-backed diff review", "clean review may legitimately produce zero findings"):
        if phrase.lower() not in validation.lower():
            errors.append(f"diff-review contract missing phrase: {phrase}")
    for phrase in (
        "Version-aware authoritative-source verification",
        "Incremental execution for non-trivial changes",
        "Compatibility-safe migrations and cutovers",
        "Dependency and toolchain changes",
    ):
        if phrase.lower() not in workflow.lower():
            errors.append(f"workflow v0.7 contract missing phrase: {phrase}")
    for phrase in (
        "Validation cadence and evidence freshness",
        "Quality-bar integrity review",
        "Baseline ratchets without invented targets",
    ):
        if phrase.lower() not in validation.lower():
            errors.append(f"validation v0.7 contract missing phrase: {phrase}")
    for phrase in (
        "Evidence-or-zero",
        "Compound obligation decomposition",
        "Verification precision gaps",
        "Risk-based discrimination checks",
    ):
        if phrase.lower() not in tests.lower():
            errors.append(f"test v0.8 evidence contract missing phrase: {phrase}")
    for phrase in (
        "Probe before `unavailable`",
        "evidence-or-zero",
        "decompose compound/enumerated requirements",
    ):
        if phrase.lower() not in validation.lower():
            errors.append(f"validation v0.8 evidence contract missing phrase: {phrase}")
    for phrase in ("Session handoff and resume", ".implement-issue/HANDOFF.md", "resume hypothesis"):
        if phrase.lower() not in workflow.lower():
            errors.append(f"workflow v0.8 handoff contract missing phrase: {phrase}")
    gates = (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
    for phrase in ("hard-to-reverse implementation decisions", "genuine one-way doors"):
        if phrase.lower() not in gates.lower():
            errors.append(f"human-gate v0.8 contract missing phrase: {phrase}")

    evidence = (ROOT / "core/EVIDENCE_MODEL.md").read_text(encoding="utf-8")
    lifecycle = (ROOT / "core/ISSUE_LIFECYCLE.md").read_text(encoding="utf-8")
    for phrase in (
        "behavior delta model",
        "current contract -> requested delta -> intended resulting contract",
        "preservation obligations",
        "A modification is not permission to drop unspecified behavior",
        "issue intent/scope drift",
        "Preserve **scope integrity**",
        "Reference scope is not mutation scope",
        "Scale planning depth to risk and ambiguity",
        "Overlap alone is not an implicit dependency",
    ):
        if phrase.lower() not in workflow.lower():
            errors.append(f"workflow v0.9 delta/coherence contract missing phrase: {phrase}")
    for phrase in (
        "Behavior-delta test semantics",
        "observable behavior/contract",
        "scenario/obligation loss is a regression",
    ):
        if phrase.lower() not in tests.lower():
            errors.append(f"test v0.9 delta contract missing phrase: {phrase}")
    for phrase in (
        "Partial evidence is not full verification",
        "Compact output must be a projection of the complete validation result",
        "material diff change needs justification traceability",
        "Behavior-delta verification",
        "Change coherence review",
        "preservation obligations remain intact",
    ):
        if phrase.lower() not in validation.lower():
            errors.append(f"validation v0.9 coherence contract missing phrase: {phrase}")
    for phrase in ("Partial evidence", "Mutable evidence and conversation memory"):
        if phrase.lower() not in evidence.lower():
            errors.append(f"evidence v0.9 contract missing phrase: {phrase}")
    for phrase in ("Gate H — material issue intent/scope drift", "Do **not** gate ordinary replanning"):
        if phrase.lower() not in gates.lower():
            errors.append(f"human-gate v0.9 contract missing phrase: {phrase}")
    for phrase in ("intent and scope identity", "coordination risk", "Do not infer a dependency or execution order"):
        if phrase.lower() not in lifecycle.lower():
            errors.append(f"lifecycle v0.9 contract missing phrase: {phrase}")

    for phrase in (
        "Solution economy and root-cause placement",
        "Existing project capability",
        "Runtime/platform capability",
        "Already-approved dependency",
        "ownership and justified complexity",
        "smallest common correct enforcement point",
        "Delegation constraint continuity",
        "Delegation is optional",
        "cannot approve a human gate",
    ):
        if phrase.lower() not in workflow.lower():
            errors.append(f"workflow v0.10 solution-economy contract missing phrase: {phrase}")
    for phrase in (
        "Proof floor before solution economy",
        "proof obligations, not bloat metrics",
        "Fewer lines, files, dependencies, abstractions, turns, tokens, or lower cost never compensate",
    ):
        if phrase.lower() not in tests.lower():
            errors.append(f"test v0.10 proof-floor contract missing phrase: {phrase}")
    for phrase in (
        "Solution-economy / ownership review",
        "Do **not** use raw LOC, file count, deletion count, or dependency count as quality scores",
        "material known operational ceiling",
        "evidence-based revisit trigger",
    ):
        if phrase.lower() not in validation.lower():
            errors.append(f"validation v0.10 solution-economy contract missing phrase: {phrase}")


    for phrase in (
        "new decision-relevant information",
        "State each material fact once",
        "semantic compression floor",
        "Do not invent opaque shorthand solely to save tokens",
        "source-side narrowing/projection",
    ):
        if phrase.lower() not in workflow.lower():
            errors.append(f"workflow v0.12 output-economy contract missing phrase: {phrase}")
    for phrase in (
        "decisive result",
        "shortest useful failure/error/location evidence",
        "preserve material semantic qualifiers",
        "a shorter statement that changes meaning is a validation/reporting defect",
    ):
        if phrase.lower() not in validation.lower():
            errors.append(f"validation v0.12 output-economy contract missing phrase: {phrase}")

    for phrase in (
        "approval scope integrity",
        "authorization is bound to the material action/decision and target",
        "prior approval is stale",
        "Equivalent local/reversible execution details do not create a new gate",
    ):
        if phrase.lower() not in workflow.lower():
            errors.append(f"workflow v0.11 approval-scope contract missing phrase: {phrase}")
    for phrase in (
        "Approval scope integrity",
        "material action or decision actually presented for review",
        "treat the approval as **stale**",
        "ordinary reversible implementation details",
    ):
        if phrase.lower() not in gates.lower():
            errors.append(f"human-gate v0.11 approval-scope contract missing phrase: {phrase}")
    for phrase in (
        "Approval freshness for gated actions",
        "validate approval freshness immediately before execution",
        "mark the prior approval stale",
        "not a requirement for hashes",
    ):
        if phrase.lower() not in validation.lower():
            errors.append(f"validation v0.11 approval-scope contract missing phrase: {phrase}")


def check_learning_contract(errors: list[str]) -> None:
    learning = (ROOT / "core/CONTINUOUS_IMPROVEMENT.md").read_text(encoding="utf-8")
    gates = (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
    for phrase in (".implement-issue/proposals/", ".implement-issue/LEARNINGS.md", "explicit human approval"):
        if phrase not in learning:
            errors.append(f"persistent learning contract missing phrase: {phrase}")
    for phrase in ("Generic-change admission check", "Merge first", "marginal benefit does not justify its ongoing complexity", "Procedure portability", "Recurrence strengthens evidence, not authority", "Failure to demonstrate benefit is valid evidence for non-adoption", "null result"):
        if phrase.lower() not in learning.lower():
            errors.append(f"anti-bloat learning contract missing phrase: {phrase}")
    for phrase in (
        "Token-economy admission",
        "net benefit",
        "recurring instruction/context overhead",
        "minimal terse control",
        "marginal benefit",
        "Do not invent a numeric savings claim",
    ):
        if phrase.lower() not in learning.lower():
            errors.append(f"continuous-improvement v0.12 token-economy contract missing phrase: {phrase}")
    if "Persistence and adoption are distinct decisions" not in gates:
        errors.append("human gate must separate learning persistence from adoption")


def check_eval_coverage(errors: list[str]) -> None:
    scenarios = sorted((ROOT / "evals/scenarios").glob("*.md"))
    if len(scenarios) != 49:
        errors.append(f"expected 49 behavioral eval scenarios, found {len(scenarios)}")
    if not (ROOT / "scripts/run_evals.py").is_file():
        errors.append("deterministic contract eval runner missing")
    live_scenarios = sorted((ROOT / "evals/live/scenarios").glob("*/scenario.json"))
    if len(live_scenarios) < 6:
        errors.append(f"expected at least 6 live-agent eval scenarios, found {len(live_scenarios)}")
    if not (ROOT / "scripts/run_live_evals.py").is_file():
        errors.append("live-agent eval runner missing")

    live_readme = (ROOT / "evals/live/README.md").read_text(encoding="utf-8")
    live_runner = (ROOT / "scripts/run_live_evals.py").read_text(encoding="utf-8")
    for phrase in (
        "intervention isolation is verified",
        "Evaluation instrument calibration",
        "known-good/positive control",
        "known-bad/negative control",
        "Null and negative results",
    ):
        if phrase.lower() not in live_readme.lower():
            errors.append(f"live-eval v0.10 methodology missing phrase: {phrase}")
    for phrase in (
        "verified runner isolation evidence",
        "verified isolation requires concrete evidence",
    ):
        if phrase.lower() not in live_runner.lower():
            errors.append(f"live-eval v0.10 isolation contract missing phrase: {phrase}")

    live_rubric = (ROOT / "evals/live/rubric.md").read_text(encoding="utf-8")
    for phrase in (
        "whole intervention",
        "minimal terse control",
        "not net-better",
    ):
        if phrase.lower() not in live_readme.lower():
            errors.append(f"live-eval v0.12 token-economy methodology missing phrase: {phrase}")
    for phrase in (
        "semantic qualifiers",
        "narration of routine tool mechanics",
    ):
        if phrase.lower() not in live_rubric.lower():
            errors.append(f"live-eval v0.12 communication rubric missing phrase: {phrase}")


def check_human_gates(errors: list[str]) -> None:
    text = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8") + (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
    for phrase in ("PROJECT_PROFILE", "PROJECT_BLUEPRINT", "Done", "human"):
        if phrase not in text:
            errors.append(f"human gate contract missing phrase: {phrase}")


def check_manifest(errors: list[str]) -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if manifest.get("version") != version:
        errors.append("manifest.json version does not match VERSION")
    if manifest.get("name") != "issuecraft-workflow":
        errors.append("manifest name must be issuecraft-workflow")
    if manifest.get("canonical_entry") != "core/WORKFLOW.md":
        errors.append("manifest canonical_entry must be core/WORKFLOW.md")


def check_readmes(errors: list[str]) -> None:
    for name in ("README.md", "README.pt-BR.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        for phrase in ("IssueCraft Workflow", "git clone https://github.com/portoduque/issuecraft-workflow.git", "cd issuecraft-workflow", "scripts/install.py", "$implement-issue", "/implement-issue", "PROJECT_PROFILE", "PROJECT_BLUEPRINT", "In Review", "Done", "LEARNINGS.md", "--overwrite-system"):
            if phrase not in text:
                errors.append(f"{name} onboarding missing: {phrase}")
        if "<REPOSITORY_URL>" in text or "<URL_DO_REPOSITORIO>" in text:
            errors.append(f"{name} still contains clone URL placeholder")


def check_ci_hardening(errors: list[str]) -> None:
    text = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    for os_name in ("ubuntu-latest", "macos-latest", "windows-latest"):
        if os_name not in text:
            errors.append(f"CI matrix missing OS: {os_name}")
    if "persist-credentials: false" not in text:
        errors.append("checkout must disable persisted credentials")
    uses_lines = [line for line in text.splitlines() if line.strip().startswith("uses:")]
    for line in uses_lines:
        if not ACTION_REF.match(line):
            errors.append(f"GitHub Action is not pinned to an immutable SHA: {line.strip()}")
    if "python scripts/run_evals.py" not in text:
        errors.append("CI must execute deterministic contract evals")
    if "python scripts/run_live_evals.py validate" not in text:
        errors.append("CI must validate live-agent eval scenarios offline")


def check_release_hardening(errors: list[str]) -> None:
    text = (ROOT / "scripts/release_zip.py").read_text(encoding="utf-8")
    if '".git"' not in text:
        errors.append("release ZIP must exclude .git")
    if "issuecraft-workflow-" not in text:
        errors.append("release ZIP must use IssueCraft artifact name")


def validate() -> list[str]:
    errors: list[str] = []
    check_required(errors)
    if errors:
        return errors
    check_json(errors)
    check_skills(errors)
    check_core_neutrality(errors)
    check_quality_contracts(errors)
    check_learning_contract(errors)
    check_eval_coverage(errors)
    check_human_gates(errors)
    check_manifest(errors)
    check_readmes(errors)
    check_ci_hardening(errors)
    check_release_hardening(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
