from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SemanticCapabilityContractTests(unittest.TestCase):
    def test_semantic_capabilities_are_optional_and_provider_neutral(self) -> None:
        text = (ROOT / "core/CAPABILITIES.md").read_text(encoding="utf-8")

        for phrase in (
            "code.structure.read",
            "code.structure.edit",
            "code.diagnostics.read",
            "semantic inspection is an optimization, not a prerequisite",
            "Do not force it for documentation, configuration, simple text edits",
            "changed regions and their enclosing semantic units",
            "without letting one large surface silently starve the others",
            "make truncation or omission explicit",
            "never assume a semantic tool is complete or authoritative by itself",
            "otherwise fall back to ordinary editing plus focused validation",
            "should trigger a retrieval-strategy change",
            "do not replace the applicable project test/build/static-analysis/review checks",
        ):
            self.assertIn(phrase.lower(), text.lower())

        for product_term in ("serena", "code-review-graph", "tree-sitter", "jetbrains", "codex", "claude", "antigravity"):
            self.assertNotIn(product_term, text.lower())

    def test_derived_evidence_requires_freshness_coverage_and_completeness(self) -> None:
        text = (ROOT / "core/EVIDENCE_MODEL.md").read_text(encoding="utf-8")

        for phrase in (
            "A bounded, paginated, truncated, sampled, or partially readable result remains partial evidence",
            "Derived/indexed evidence integrity",
            "subject freshness",
            "completeness limits",
            "known blind spots",
            "A zero/empty derived result supports `absent` only",
            "not_detected",
            "Evaluation evidence independence",
            "derived wholly or partly from the same mechanism being evaluated",
            "consistency/upper-bound evidence rather than independent proof of correctness",
        ):
            self.assertIn(phrase.lower(), text.lower())

    def test_progressive_context_scenario_covers_semantic_fallback_and_safety(self) -> None:
        text = (ROOT / "evals/scenarios/19-progressive-context-impact.md").read_text(encoding="utf-8")

        for phrase in (
            "Prefer semantic/structural retrieval",
            "fall back cleanly",
            "changed region -> enclosing semantic unit -> materially relevant relationships",
            "preserving enough breadth",
            "Make truncation, omitted regions, bounded result sets",
            "useful evidence rather than infallible ground truth",
            "Before a structure-aware mutation",
            "Change retrieval strategy",
            "Let one large or high-risk file consume the entire retrieval budget",
            "Treat a truncated, capped, paginated, or otherwise partial result as proof",
            "Require semantic tooling as a prerequisite",
            "Force semantic tooling onto documentation, configuration, or simple text edits",
            "Treat semantic diagnostics as a substitute",
        ):
            self.assertIn(phrase.lower(), text.lower())


if __name__ == "__main__":
    unittest.main()
