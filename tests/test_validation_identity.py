from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ValidationIdentityContractTests(unittest.TestCase):
    def test_final_validation_is_bound_to_a_material_subject(self):
        validation = read("core/VALIDATION.md")
        workflow = read("core/WORKFLOW.md")
        gates = read("core/HUMAN_GATES.md")

        for phrase in (
            "Validation subject identity",
            "the materially relevant implementation state",
            "strongest practical identity",
            "material subject change makes the prior PASS stale",
            "Do **not** require a universal content hash",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        for phrase in (
            "capture/reconcile the validation subject",
            "a result for a materially different subject is stale",
            "Passed but subject materially changed",
            "Do not transfer the old PASS to different work",
        ):
            self.assertIn(phrase.lower(), workflow.lower())

        for phrase in (
            "validation subject the human actually reviewed",
            "the prior PASS is stale",
            "Do not require a universal hash, lock, or frozen candidate",
        ):
            self.assertIn(phrase.lower(), gates.lower())

    def test_validation_evidence_keeps_origin_and_freshness(self):
        validation = read("core/VALIDATION.md")
        report = read("templates/ISSUE_EXECUTION_REPORT.md")

        for phrase in (
            "evidence origin",
            "CI/external evidence",
            "reused earlier evidence",
            "freshness rationale",
            "Do not relabel reused or externally supplied evidence as a new execution",
            "Unknown evidence origin or an unbound subject is not positive proof",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        for phrase in (
            "Validation subject / evidence provenance",
            "Evidence executed for this subject",
            "CI/external evidence and subject binding",
            "Reused evidence, original subject/revision, and freshness rationale",
            "Unknown/unbound evidence limitations",
        ):
            self.assertIn(phrase.lower(), report.lower())

    def test_impact_is_scaled_by_behavioral_reach_not_file_shape(self):
        workflow = read("core/WORKFLOW.md")
        for phrase in (
            "behavioral reach",
            "Do not use diff size, file count, filename extension",
            "Prompts, agent/skill instructions, configuration, schemas, templates, generator inputs, and build/CI definitions are behavioral inputs",
            "a tiny textual change can therefore require broader evidence",
        ):
            self.assertIn(phrase.lower(), workflow.lower())

    def test_differential_verification_is_optional_and_baseline_bound(self):
        validation = read("core/VALIDATION.md")
        report = read("templates/ISSUE_EXECUTION_REPORT.md")

        for phrase in (
            "Optional differential verification",
            "same representative input",
            "intended by the requested delta",
            "unexpected differences requiring investigation",
            "Do not require differential testing for every issue",
            "does **not** prove compatibility",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        self.assertIn("Differential verification performed", report)

    def test_manual_plan_records_subject_and_stale_pass_rule(self):
        plan = read("templates/MANUAL_VALIDATION_PLAN.md")
        for phrase in (
            "## Validation subject",
            "strongest practical identity",
            "Working-tree/material changed-state note",
            "A PASS applies only to the validation subject above",
            "mark the prior PASS stale",
        ):
            self.assertIn(phrase.lower(), plan.lower())

    def test_live_done_gate_exercises_subject_refresh_after_fix(self):
        scenario = json.loads(
            read("evals/live/scenarios/human-done-gate/scenario.json")
        )
        criteria = {item["id"]: item for item in scenario["criteria"]}
        self.assertIn("manual-pass-subject-binding", criteria)
        criterion = criteria["manual-pass-subject-binding"]
        self.assertEqual("blocker", criterion["severity"])
        text = criterion["text"].lower()
        self.assertIn("failed manual validation", text)
        self.assertIn("refreshes or reconciles", text)
        self.assertIn("materially changed subject", text)
        self.assertIn("remain in review", text)

    def test_new_contract_does_not_add_runtime_or_provider_coupling(self):
        validation = read("core/VALIDATION.md").lower()
        workflow = read("core/WORKFLOW.md").lower()
        gates = read("core/HUMAN_GATES.md").lower()
        combined = "\n".join((validation, workflow, gates))

        for forbidden in (
            "mandatory sha-256",
            "mandatory hash",
            "lock server required",
            "central validation database",
            "automatic worktree",
        ):
            self.assertNotIn(forbidden, combined)

        self.assertIn("do **not** require a universal content hash", validation)
        self.assertIn("do not require a universal hash, lock, or frozen candidate", gates)


if __name__ == "__main__":
    unittest.main()
