from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RenderedEvidenceAndDecisionQualityTests(unittest.TestCase):
    def test_rendered_surface_evidence_is_risk_based_and_not_source_only(self) -> None:
        validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
        scenario = (ROOT / "evals/scenarios/20-test-evidence-quality.md").read_text(encoding="utf-8")

        for phrase in (
            "Rendered-surface evidence",
            "source inspection alone is insufficient proof",
            "lowest-cost rendered/runtime evidence",
            "Do not invent a universal visual matrix",
            "surface/state it actually captures",
            "Do not turn the agent's aesthetic preference into a defect",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        for phrase in (
            "rendered/runtime evidence",
            "partial evidence",
            "project/issue evidence",
            "subjective aesthetic preference",
        ):
            self.assertIn(phrase.lower(), scenario.lower())

    def test_human_decisions_are_evidence_first_and_dependency_aware(self) -> None:
        gates = (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
        scenario = (ROOT / "evals/scenarios/33-one-way-door-gate.md").read_text(encoding="utf-8")

        for phrase in (
            "Decision-request quality",
            "Resolve what current repository/project evidence can answer safely",
            "upstream decision",
            "re-evaluate downstream questions",
            "recommend it and state the evidence/rationale",
            "does not create new gates",
        ):
            self.assertIn(phrase.lower(), gates.lower())

        for phrase in (
            "repository/project-answerable facts",
            "ask the upstream decision first",
            "evidence-backed recommendation",
            "Invent certainty",
        ):
            self.assertIn(phrase.lower(), scenario.lower())


if __name__ == "__main__":
    unittest.main()
