import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvidenceApplicabilityAndLayeredConfigTests(unittest.TestCase):
    def test_derived_evidence_requires_applicability_before_use(self) -> None:
        evidence = (ROOT / "core/EVIDENCE_MODEL.md").read_text(encoding="utf-8")
        scenario = (ROOT / "evals/scenarios/19-progressive-context-impact.md").read_text(encoding="utf-8")

        for phrase in (
            "applicability",
            "subject, scope, version/environment, mode/platform",
            "high-ranked, nearest, or otherwise retrieved recommendation is not automatically a project fact",
            "narrow or reframe retrieval",
            "explicitly unverified/fallback",
        ):
            self.assertIn(phrase.lower(), evidence.lower())

        self.assertIn("useful evidence rather than infallible ground truth", scenario.lower())

    def test_layered_configuration_resolves_effective_value_before_shared_mutation(self) -> None:
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        scenario = (ROOT / "evals/scenarios/42-root-cause-placement.md").read_text(encoding="utf-8")

        for phrase in (
            "effective configuration at the affected scope",
            "evidenced precedence",
            "narrowest authoritative layer",
            "broader/base layer only when evidence shows the invariant is genuinely shared",
            "validate the materially affected siblings",
        ):
            self.assertIn(phrase.lower(), workflow.lower())

        for phrase in (
            "resolve the effective configuration at the affected scope",
            "establish evidenced precedence",
            "narrowest authoritative configuration layer",
            "assume the first/global/base configuration value found is the effective value",
        ):
            self.assertIn(phrase.lower(), scenario.lower())


if __name__ == "__main__":
    unittest.main()
