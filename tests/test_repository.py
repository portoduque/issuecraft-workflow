import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_repo.py")
validator = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(validator)

spec2 = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(spec2)
assert spec2.loader
spec2.loader.exec_module(installer)


class RepositoryTests(unittest.TestCase):
    def test_structural_validator(self):
        self.assertEqual([], validator.validate())

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
            profile.write_text("sentinel: keep\n", encoding="utf-8")

            installer.install(target)
            self.assertEqual("sentinel: keep\n", profile.read_text(encoding="utf-8"))
            self.assertTrue((state / "system/core/WORKFLOW.md").is_file())
            self.assertTrue((state / "system/core/SECURITY.md").is_file())
            self.assertTrue((state / "system/core/PERFORMANCE.md").is_file())
            self.assertTrue((state / "system/core/TEST_STRATEGY.md").is_file())
            self.assertTrue((target / ".agents/skills/implement-issue/SKILL.md").is_file())
            self.assertTrue((target / ".claude/skills/implement-issue/SKILL.md").is_file())

    def test_install_does_not_create_profile_or_blueprint(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            installer.install(target)
            state = target / ".implement-issue"
            self.assertFalse((state / "PROJECT_PROFILE.yaml").exists())
            self.assertFalse((state / "PROJECT_BLUEPRINT.yaml").exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink support required")
    def test_installer_refuses_managed_symlink(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside_td:
            target = Path(td)
            outside = Path(outside_td)
            (target / ".agents").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(SystemExit):
                installer.install(target)
            self.assertFalse((outside / "skills/implement-issue/SKILL.md").exists())

    def test_readme_has_fast_onboarding_and_core_guarantees(self):
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        portuguese = (ROOT / "README.pt-BR.md").read_text(encoding="utf-8")

        for readme in (english, portuguese):
            self.assertIn("git clone", readme)
            self.assertIn("scripts/install.py", readme)
            self.assertIn("$implement-issue", readme)
            self.assertIn("/implement-issue", readme)
            self.assertIn("PROJECT_PROFILE", readme)
            self.assertIn("PROJECT_BLUEPRINT", readme)
            self.assertIn("In Review", readme)
            self.assertIn("Done", readme)
            self.assertIn("SECURITY.md", readme)
            self.assertIn("PERFORMANCE.md", readme)
            self.assertIn("TEST_STRATEGY.md", readme)
            self.assertIn("--overwrite-system", readme)

    def test_quality_eval_scenarios_exist(self):
        for n in range(11, 17):
            matches = list((ROOT / "evals/scenarios").glob(f"{n:02d}-*.md"))
            self.assertEqual(1, len(matches), f"missing or duplicate eval for {n:02d}")


if __name__ == "__main__":
    unittest.main()
