from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CompactToolEvidenceContractTests(unittest.TestCase):
    def test_capabilities_prefer_faithful_structured_output_and_recoverable_projection(self) -> None:
        text = (ROOT / "core/CAPABILITIES.md").read_text(encoding="utf-8")

        for phrase in (
            "stable machine-readable representation",
            "does not change the operation or omit required diagnostics",
            "fall back to the strongest faithful representation available",
            "fresh complete artifact/result remains addressable",
            "before rerunning an unchanged operation solely to recover output",
            "unexpectedly empty",
            "contradicts trustworthy status/control signals",
            "without a recoverable source",
        ):
            self.assertIn(phrase.lower(), text.lower())

    def test_semantic_output_scenario_preserves_recovery_and_fidelity(self) -> None:
        text = (ROOT / "evals/scenarios/48-semantic-output-economy.md").read_text(encoding="utf-8")

        for phrase in (
            "stable machine-readable tool representation",
            "fall back to a more faithful representation",
            "fresh complete artifact/result",
            "Rerun an unchanged expensive operation solely to recover detail",
            "irrecoverably truncated or internally inconsistent compact output",
        ):
            self.assertIn(phrase.lower(), text.lower())

    def test_token_economy_counts_reexpansion_cost_without_fixed_threshold(self) -> None:
        learning = (ROOT / "core/CONTINUOUS_IMPROVEMENT.md").read_text(encoding="utf-8")
        scenario = (ROOT / "evals/scenarios/49-token-economy-evidence.md").read_text(encoding="utf-8")

        for phrase in (
            "Repeated immediate re-expansion",
            "extra retrieval, tool work, and turn cost",
            "Do not impose a universal re-expansion-rate threshold",
        ):
            self.assertIn(phrase.lower(), learning.lower())

        for phrase in (
            "repeated immediate re-expansion or retrieval",
            "include the resulting tool/turn cost",
            "universal re-expansion-rate threshold",
        ):
            self.assertIn(phrase.lower(), scenario.lower())


if __name__ == "__main__":
    unittest.main()
