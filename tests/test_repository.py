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
        self.assertEqual(17, len(contract_evals.EVALS))
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
            for rel in ("PROJECT_PROFILE.yaml", "PROJECT_BLUEPRINT.yaml", "PROJECT_RULES.md", "LEARNINGS.md", "proposals"):
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
