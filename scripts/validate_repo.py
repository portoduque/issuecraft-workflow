#!/usr/bin/env python3
"""Structural checks for the implement-issue workflow source repository."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "VERSION",
    "manifest.json",
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
    ".agents/skills/implement-issue/SKILL.md",
    ".claude/skills/implement-issue/SKILL.md",
]
VENDOR_TERMS = re.compile(r"\b(codex|claude|antigravity|openai|anthropic|gemini)\b", re.I)
STACK_TERMS = re.compile(
    r"\b(typescript|javascript|python|java|kotlin|swift|rust|react|django|fastapi|spring|"
    r"postgresql|mysql|mongodb|redis|npm|pnpm|yarn|pytest|jest|vitest|flyway|liquibase|prisma)\b",
    re.I,
)


def check_required(errors: list[str]) -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")


def check_json(errors: list[str]) -> None:
    for p in list((ROOT / "schemas").glob("*.json")) + [ROOT / "manifest.json"]:
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {p.relative_to(ROOT)}: {exc}")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def check_skills(errors: list[str]) -> None:
    paths = [
        ROOT / ".agents/skills/implement-issue/SKILL.md",
        ROOT / ".claude/skills/implement-issue/SKILL.md",
    ]
    texts = []
    for p in paths:
        text = p.read_text(encoding="utf-8")
        texts.append(text)
        fm = parse_frontmatter(text)
        if fm.get("name") != "implement-issue":
            errors.append(f"invalid/missing skill name in {p.relative_to(ROOT)}")
        if not fm.get("description"):
            errors.append(f"missing skill description in {p.relative_to(ROOT)}")
        if "core/WORKFLOW.md" not in text:
            errors.append(f"adapter does not delegate to canonical workflow: {p.relative_to(ROOT)}")
    if len(set(texts)) != 1:
        errors.append("agent skill adapters must be behaviorally identical")


def check_core_neutrality(errors: list[str]) -> None:
    for p in (ROOT / "core").glob("*.md"):
        text = p.read_text(encoding="utf-8")
        m = VENDOR_TERMS.search(text)
        if m:
            errors.append(f"provider term '{m.group(0)}' leaked into canonical core: {p.relative_to(ROOT)}")
        m = STACK_TERMS.search(text)
        if m:
            errors.append(f"stack-specific term '{m.group(0)}' leaked into canonical core: {p.relative_to(ROOT)}")


def check_quality_contracts(errors: list[str]) -> None:
    workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
    validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
    tests = (ROOT / "core/TEST_STRATEGY.md").read_text(encoding="utf-8")
    security = (ROOT / "core/SECURITY.md").read_text(encoding="utf-8")
    performance = (ROOT / "core/PERFORMANCE.md").read_text(encoding="utf-8")
    required_workflow_refs = ["TEST_STRATEGY.md", "SECURITY.md", "PERFORMANCE.md", "security-impact triage", "performance-impact triage"]
    for phrase in required_workflow_refs:
        if phrase not in workflow:
            errors.append(f"workflow quality contract missing phrase: {phrase}")
    required_test_terms = ["Unit", "Integration", "Contract", "End-to-end", "Regression", "property-based", "fuzz", "mutation", "concurrency", "accessibility", "load", "stress", "soak", "compatibility", "migration"]
    for phrase in required_test_terms:
        if phrase.lower() not in tests.lower():
            errors.append(f"test taxonomy missing category: {phrase}")
    if "material security regression" not in security:
        errors.append("security blocker contract missing")
    if "performance budget" not in performance:
        errors.append("performance budget contract missing")
    if "not_applicable" not in validation or "unavailable" not in validation:
        errors.append("validation must distinguish not_applicable from unavailable")


def check_eval_coverage(errors: list[str]) -> None:
    required = [
        "11-security-sensitive.md",
        "12-performance-sensitive.md",
        "13-test-taxonomy.md",
        "14-agent-neutrality.md",
        "15-stack-neutrality.md",
        "16-safe-expensive-tests.md",
    ]
    for name in required:
        if not (ROOT / "evals/scenarios" / name).is_file():
            errors.append(f"missing quality regression eval: {name}")


def check_human_gates(errors: list[str]) -> None:
    workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
    gates = (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
    required_phrases = ["PROJECT_PROFILE", "PROJECT_BLUEPRINT", "Done", "human"]
    for phrase in required_phrases:
        if phrase not in workflow + gates:
            errors.append(f"human gate contract missing phrase: {phrase}")


def check_manifest(errors: list[str]) -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if manifest.get("version") != version:
        errors.append("manifest.json version does not match VERSION")
    if manifest.get("canonical_entry") != "core/WORKFLOW.md":
        errors.append("manifest canonical_entry must be core/WORKFLOW.md")


def validate() -> list[str]:
    errors: list[str] = []
    check_required(errors)
    if errors:
        return errors
    check_json(errors)
    check_skills(errors)
    check_core_neutrality(errors)
    check_quality_contracts(errors)
    check_eval_coverage(errors)
    check_human_gates(errors)
    check_manifest(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("VALIDATION FAILED")
        for err in errors:
            print(f"- {err}")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
