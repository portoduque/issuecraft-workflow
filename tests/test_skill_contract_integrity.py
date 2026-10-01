from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractIntegrityTests(unittest.TestCase):
    def test_live_eval_contract_is_black_box_behavior_first(self) -> None:
        live = (ROOT / "evals/live/README.md").read_text(encoding="utf-8")
        rubric = (ROOT / "evals/live/rubric.md").read_text(encoding="utf-8")
        scenario = (ROOT / "evals/scenarios/46-live-eval-methodology.md").read_text(
            encoding="utf-8"
        )

        for phrase in (
            "Black-box behavioral criteria",
            "externally observable repository/task outcomes",
            "canonical IssueCraft terminology",
            "Deterministic contract evals",
        ):
            self.assertIn(phrase.lower(), live.lower())

        for phrase in (
            "observable task/repository outcomes",
            "Do not reward a candidate merely for naming an internal workflow concept",
            "deterministic contract evals",
        ):
            self.assertIn(phrase.lower(), rubric.lower())

        for phrase in (
            "externally observable repository/task outcomes",
            "deterministic contract evals",
            "Reward a candidate merely for echoing workflow terminology",
        ):
            self.assertIn(phrase.lower(), scenario.lower())

    def test_compatibility_smoke_covers_implicit_routing_boundaries(self) -> None:
        text = (ROOT / "docs/compatibility-release.md").read_text(encoding="utf-8")
        for phrase in (
            "Implicit routing smoke",
            "positive trigger",
            "negative adjacent prompt",
            "without explicitly naming the skill",
            "not_applicable",
            "do not infer success from explicit invocation",
        ):
            self.assertIn(phrase.lower(), text.lower())

    def test_direct_normative_references_resolve(self) -> None:
        adapters = (
            ROOT / ".agents/skills/implement-issue/SKILL.md",
            ROOT / ".claude/skills/implement-issue/SKILL.md",
        )
        source_pointer = "../../../core/WORKFLOW.md"
        expected_workflow = (ROOT / "core/WORKFLOW.md").resolve()

        for adapter in adapters:
            text = adapter.read_text(encoding="utf-8")
            self.assertIn(source_pointer, text)
            self.assertEqual(expected_workflow, (adapter.parent / source_pointer).resolve())
            self.assertTrue((adapter.parent / source_pointer).is_file())

        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        start_marker = "Use these supporting documents when their phase is reached:"
        self.assertIn(start_marker, workflow)
        section = workflow.split(start_marker, 1)[1].split("\n## 1.", 1)[0]
        direct_docs = re.findall(r"`([A-Z][A-Z_]+\.md)`", section)
        self.assertGreater(len(direct_docs), 0)

        for filename in direct_docs:
            with self.subTest(filename=filename):
                self.assertTrue(
                    (ROOT / "core" / filename).is_file(),
                    f"direct workflow reference does not resolve: core/{filename}",
                )


if __name__ == "__main__":
    unittest.main()
