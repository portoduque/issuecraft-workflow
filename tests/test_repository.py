import importlib.util
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


validator = load_module("validator", ROOT / "scripts/validate_repo.py")
installer = load_module("installer", ROOT / "scripts/install.py")
contract_evals = load_module("contract_evals", ROOT / "scripts/run_evals.py")
release_zip = load_module("release_zip", ROOT / "scripts/release_zip.py")


class RepositoryTests(unittest.TestCase):
    def test_structural_validator(self):
        self.assertEqual([], validator.validate())

    def test_contract_evals_execute_all_scenarios(self):
        self.assertEqual(46, len(contract_evals.EVALS))
        self.assertEqual([], contract_evals.run())

    def test_agent_adapters_are_identical_and_delegate_to_core(self):
        a = (ROOT / ".agents/skills/implement-issue/SKILL.md").read_text(encoding="utf-8")
        c = (ROOT / ".claude/skills/implement-issue/SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(a, c)
        self.assertIn("core/WORKFLOW.md", a)

    def test_canonical_core_is_provider_and_stack_neutral(self):
        for path in (ROOT / "core").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(validator.VENDOR_TERMS.search(text), path.name)
            self.assertIsNone(validator.STACK_TERMS.search(text), path.name)

    def test_quality_contract_is_first_class(self):
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        for required in ("TEST_STRATEGY.md", "SECURITY.md", "PERFORMANCE.md", "security-impact triage", "performance-impact triage"):
            self.assertIn(required, workflow)

        tests = (ROOT / "core/TEST_STRATEGY.md").read_text(encoding="utf-8").lower()
        for category in ("unit", "integration", "contract", "end-to-end", "regression", "property-based", "fuzz", "mutation", "concurrency", "accessibility", "load", "stress", "soak", "compatibility", "migration"):
            self.assertIn(category, tests)

    def test_output_efficiency_preserves_evidence(self):
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
        for phrase in (
            "Compress presentation, never evidence",
            "delta-only progress updates",
            "Do not duplicate",
            "Group routine successful checks",
            "one concrete next action",
        ):
            self.assertIn(phrase, workflow)
        for phrase in (
            "Preserve complete validation evidence",
            "Never collapse `unavailable`",
            "Token/output reduction is never a reason to omit material evidence",
        ):
            self.assertIn(phrase, validation)

    def test_evidence_driven_execution_and_test_quality_contracts(self):
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        tests = (ROOT / "core/TEST_STRATEGY.md").read_text(encoding="utf-8")
        validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
        learning = (ROOT / "core/CONTINUOUS_IMPROVEMENT.md").read_text(encoding="utf-8")

        for phrase in (
            "diagnostic reset",
            "Retrieve context progressively",
            "highest-signal evidence",
            "risk-based impact reconnaissance",
        ):
            self.assertIn(phrase.lower(), workflow.lower())

        for phrase in (
            "Behavior-to-evidence traceability",
            "lowest-cost test layer that can faithfully prove the behavior",
            "materially discriminate correct behavior",
            "path parity",
            "Mocks, fakes, stubs",
            "Instrumented runtime diagnostics",
            "critical cross-layer journeys",
        ):
            self.assertIn(phrase.lower(), tests.lower())

        for phrase in (
            "Evidence-backed diff review",
            "clean review may legitimately produce zero findings",
            "preserve/reference the useful artifacts",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        for phrase in (
            "Generic-change admission check",
            "Merge first",
            "marginal benefit does not justify its ongoing complexity",
        ):
            self.assertIn(phrase.lower(), learning.lower())

    def test_v07_execution_validation_and_portability_contracts(self):
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
        learning = (ROOT / "core/CONTINUOUS_IMPROVEMENT.md").read_text(encoding="utf-8")

        for phrase in (
            "Version-aware authoritative-source verification",
            "Incremental execution for non-trivial changes",
            "risk-first slice",
            "Compatibility-safe migrations and cutovers",
            "Dependency and toolchain changes",
        ):
            self.assertIn(phrase.lower(), workflow.lower())

        for phrase in (
            "Validation cadence and evidence freshness",
            "Quality-bar integrity review",
            "Baseline ratchets without invented targets",
            "Do not repeat an unchanged green command",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        for phrase in (
            "Procedure portability",
            "generic engineering procedure",
            "could the rule still be justified without naming the model/host/tool",
        ):
            self.assertIn(phrase.lower(), learning.lower())

    def test_v08_evidence_handoff_and_one_way_door_contracts(self):
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        tests = (ROOT / "core/TEST_STRATEGY.md").read_text(encoding="utf-8")
        validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
        gates = (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
        learning = (ROOT / "core/CONTINUOUS_IMPROVEMENT.md").read_text(encoding="utf-8")

        for phrase in (
            "Evidence-or-zero",
            "Compound obligation decomposition",
            "Verification precision gaps",
            "Risk-based discrimination checks",
            "isolated disposable state",
        ):
            self.assertIn(phrase.lower(), tests.lower())

        for phrase in (
            "Probe before `unavailable`",
            "safe prerequisite/capability probe",
            "decompose compound/enumerated requirements",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        for phrase in (
            "Session handoff and resume",
            ".implement-issue/HANDOFF.md",
            "resume hypothesis",
            "current evidence win over stale narrative",
        ):
            self.assertIn(phrase.lower(), workflow.lower())

        for phrase in (
            "Gate G — hard-to-reverse implementation decisions",
            "genuine one-way doors",
            "ordinary local implementation choices",
        ):
            self.assertIn(phrase.lower(), gates.lower())

        self.assertIn("Recurrence strengthens evidence, not authority".lower(), learning.lower())
        self.assertTrue((ROOT / "templates/HANDOFF.md").is_file())

    def test_v09_behavior_delta_scope_and_coherence_contracts(self):
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        tests = (ROOT / "core/TEST_STRATEGY.md").read_text(encoding="utf-8")
        validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
        evidence = (ROOT / "core/EVIDENCE_MODEL.md").read_text(encoding="utf-8")
        gates = (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
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
            self.assertIn(phrase.lower(), workflow.lower())

        for phrase in (
            "Behavior-delta test semantics",
            "observable behavior/contract",
            "scenario/obligation loss is a regression",
            "removed behavior is absent/inaccessible",
        ):
            self.assertIn(phrase.lower(), tests.lower())

        for phrase in (
            "Partial evidence is not full verification",
            "Compact output must be a projection of the complete validation result",
            "material diff change needs justification traceability",
            "Behavior-delta verification",
            "Change coherence review",
            "specific corrective action when the evidence makes one known",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        for phrase in (
            "Partial evidence",
            "Mutable evidence and conversation memory",
            "unsupported remainder unverified/unknown",
        ):
            self.assertIn(phrase.lower(), evidence.lower())

        self.assertIn("Gate H — material issue intent/scope drift".lower(), gates.lower())
        self.assertIn("Do **not** gate ordinary replanning".lower(), gates.lower())
        self.assertIn("intent and scope identity".lower(), lifecycle.lower())
        self.assertIn("Do not infer a dependency or execution order".lower(), lifecycle.lower())

        report = (ROOT / "templates/ISSUE_EXECUTION_REPORT.md").read_text(encoding="utf-8")
        manual = (ROOT / "templates/MANUAL_VALIDATION_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("Behavior delta / preservation", report)
        self.assertIn("Regression / preservation checks", manual)

    def test_v010_solution_economy_and_eval_rigor_contracts(self):
        workflow = (ROOT / "core/WORKFLOW.md").read_text(encoding="utf-8")
        tests = (ROOT / "core/TEST_STRATEGY.md").read_text(encoding="utf-8")
        validation = (ROOT / "core/VALIDATION.md").read_text(encoding="utf-8")
        learning = (ROOT / "core/CONTINUOUS_IMPROVEMENT.md").read_text(encoding="utf-8")
        live_readme = (ROOT / "evals/live/README.md").read_text(encoding="utf-8")
        live_rubric = (ROOT / "evals/live/rubric.md").read_text(encoding="utf-8")
        live_runner = (ROOT / "scripts/run_live_evals.py").read_text(encoding="utf-8")

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
            self.assertIn(phrase.lower(), workflow.lower())

        for phrase in (
            "Proof floor before solution economy",
            "proof obligations, not bloat metrics",
            "Fewer lines, files, dependencies, abstractions, turns, tokens, or lower cost never compensate",
        ):
            self.assertIn(phrase.lower(), tests.lower())

        for phrase in (
            "Solution-economy / ownership review",
            "Do **not** use raw LOC, file count, deletion count, or dependency count as quality scores",
            "material known operational ceiling",
            "evidence-based revisit trigger",
        ):
            self.assertIn(phrase.lower(), validation.lower())

        self.assertIn(
            "Failure to demonstrate benefit is valid evidence for non-adoption".lower(),
            learning.lower(),
        )
        self.assertIn("null result", learning.lower())

        for phrase in (
            "intervention isolation is verified",
            "Evaluation instrument calibration",
            "known-good/positive control",
            "known-bad/negative control",
            "Null and negative results",
        ):
            self.assertIn(phrase.lower(), live_readme.lower())

        self.assertIn("Solution economy".lower(), live_rubric.lower())
        self.assertIn("tie/null result is legitimate".lower(), live_rubric.lower())
        self.assertIn("verified runner isolation evidence".lower(), live_runner.lower())

        report = (ROOT / "templates/ISSUE_EXECUTION_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("Solution economy / known limits", report)
        self.assertIn("Evidence-based revisit trigger", report)

        self.assertTrue(
            (ROOT / "evals/live/scenarios/root-cause-shared-path/scenario.json").is_file()
        )

    def test_profile_schema_has_security_performance_and_test_discovery(self):
        schema = json.loads((ROOT / "schemas/project-profile.schema.json").read_text(encoding="utf-8"))
        observed = schema["properties"]["observed"]["properties"]
        self.assertIn("testing_tools", observed)
        self.assertIn("security_tools", observed)
        self.assertIn("performance_tools", observed)
        command_props = schema["$defs"]["command"]["properties"]
        self.assertIn("kind", command_props)
        commands = schema["properties"]["commands"]["properties"]
        for key in ("security", "benchmark", "performance", "load", "stress", "accessibility", "compatibility", "recovery"):
            self.assertIn(key, commands)

    def test_install_preserves_project_owned_state(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            state = target / ".implement-issue"
            state.mkdir()
            profile = state / "PROJECT_PROFILE.yaml"
            learning = state / "LEARNINGS.md"
            profile.write_text("sentinel: keep\n", encoding="utf-8")
            learning.write_text("learning: keep\n", encoding="utf-8")

            installer.install(target)
            self.assertEqual("sentinel: keep\n", profile.read_text(encoding="utf-8"))
            self.assertEqual("learning: keep\n", learning.read_text(encoding="utf-8"))
            self.assertTrue((state / "system/core/WORKFLOW.md").is_file())
            self.assertTrue((state / "system/core/SECURITY.md").is_file())
            self.assertTrue((state / "system/core/PERFORMANCE.md").is_file())
            self.assertTrue((state / "system/core/TEST_STRATEGY.md").is_file())
            self.assertTrue((state / "system/templates/LEARNINGS.md").is_file())

    def test_install_does_not_create_project_owned_knowledge(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            installer.install(target)
            state = target / ".implement-issue"
            for rel in ("PROJECT_PROFILE.yaml", "PROJECT_BLUEPRINT.yaml", "PROJECT_RULES.md", "LEARNINGS.md", "HANDOFF.md", "proposals"):
                self.assertFalse((state / rel).exists(), rel)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink support required")
    def test_installer_refuses_managed_symlink(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside_td:
            target = Path(td)
            outside = Path(outside_td)
            try:
                (target / ".agents").symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            with self.assertRaises(SystemExit):
                installer.install(target)
            self.assertFalse((outside / "skills/implement-issue/SKILL.md").exists())

    def test_release_zip_is_clean_and_branded(self):
        with tempfile.TemporaryDirectory() as td:
            archive = release_zip.create_release_zip(Path(td))
            self.assertTrue(archive.name.startswith("issuecraft-workflow-"))
            with zipfile.ZipFile(archive) as zf:
                names = zf.namelist()
            self.assertTrue(names)
            self.assertFalse(any("/.git/" in f"/{name}" or name.endswith("/.git") for name in names))
            self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in names))

    def test_readmes_have_copy_paste_onboarding_and_core_guarantees(self):
        for name in ("README.md", "README.pt-BR.md"):
            readme = (ROOT / name).read_text(encoding="utf-8")
            for required in (
                "IssueCraft Workflow",
                "git clone https://github.com/portoduque/issuecraft-workflow.git",
                "cd issuecraft-workflow",
                "scripts/install.py",
                "$implement-issue",
                "/implement-issue",
                "PROJECT_PROFILE",
                "PROJECT_BLUEPRINT",
                "In Review",
                "Done",
                "SECURITY.md",
                "PERFORMANCE.md",
                "TEST_STRATEGY.md",
                "LEARNINGS.md",
                "--overwrite-system",
            ):
                self.assertIn(required, readme)
            self.assertNotIn("<REPOSITORY_URL>", readme)
            self.assertNotIn("<URL_DO_REPOSITORIO>", readme)

    def test_learning_is_persistent_but_human_gated(self):
        learning = (ROOT / "core/CONTINUOUS_IMPROVEMENT.md").read_text(encoding="utf-8")
        gates = (ROOT / "core/HUMAN_GATES.md").read_text(encoding="utf-8")
        self.assertIn(".implement-issue/proposals/", learning)
        self.assertIn(".implement-issue/LEARNINGS.md", learning)
        self.assertIn("explicit human approval", learning)
        self.assertIn("Persistence and adoption are distinct decisions", gates)

    def test_ci_is_cross_platform_and_hardened(self):
        ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        for os_name in ("ubuntu-latest", "macos-latest", "windows-latest"):
            self.assertIn(os_name, ci)
        self.assertIn("persist-credentials: false", ci)
        self.assertIn("python scripts/run_evals.py", ci)
        for line in ci.splitlines():
            if line.strip().startswith("uses:"):
                self.assertRegex(line.strip(), r"^uses:\s*[^@\s]+@[0-9a-f]{40}(?:\s+#.*)?$")


if __name__ == "__main__":
    unittest.main()
