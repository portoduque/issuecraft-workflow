import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


validator = load_module("validator_resistance_target", ROOT / "scripts/validate_repo.py")


class ValidatorResistanceTests(unittest.TestCase):
    def test_validator_mutants_are_killed_and_negative_control_survives(self):
        with tempfile.TemporaryDirectory() as td:
            sandbox = Path(td) / "repo"
            shutil.copytree(
                ROOT,
                sandbox,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )

            original_root = validator.ROOT
            validator.ROOT = sandbox
            try:
                self.assertEqual([], validator.validate())

                def mutate_text(rel: str, old: str, new: str, expected: str):
                    path = sandbox / rel
                    original = path.read_text(encoding="utf-8")
                    self.assertIn(old, original, rel)
                    path.write_text(original.replace(old, new, 1), encoding="utf-8")
                    errors = validator.validate()
                    self.assertTrue(
                        any(expected.lower() in error.lower() for error in errors),
                        f"{rel} mutant survived; errors={errors}",
                    )
                    path.write_text(original, encoding="utf-8")
                    self.assertEqual([], validator.validate())

                mutate_text(
                    "core/TEST_STRATEGY.md",
                    "Evidence-or-zero",
                    "Evidence proof",
                    "test v0.8 evidence contract missing phrase: Evidence-or-zero",
                )
                mutate_text(
                    "core/VALIDATION.md",
                    "Probe before `unavailable`",
                    "Unavailable handling",
                    "validation v0.8 evidence contract missing phrase",
                )
                mutate_text(
                    "core/WORKFLOW.md",
                    "Session handoff and resume",
                    "Session continuation",
                    "workflow v0.8 handoff contract missing phrase",
                )
                mutate_text(
                    "core/HUMAN_GATES.md",
                    "hard-to-reverse implementation decisions",
                    "implementation choices",
                    "human-gate v0.8 contract missing phrase",
                )

                manifest_path = sandbox / "manifest.json"
                manifest_original = manifest_path.read_text(encoding="utf-8")
                manifest = json.loads(manifest_original)
                manifest["version"] = "mutant-version"
                manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                errors = validator.validate()
                self.assertTrue(
                    any("manifest.json version does not match VERSION" in error for error in errors),
                    f"manifest mutant survived; errors={errors}",
                )
                manifest_path.write_text(manifest_original, encoding="utf-8")
                self.assertEqual([], validator.validate())

                scenario = sandbox / "evals/scenarios/33-one-way-door-gate.md"
                scenario_bytes = scenario.read_bytes()
                scenario.unlink()
                errors = validator.validate()
                self.assertTrue(
                    any("expected 33 behavioral eval scenarios" in error for error in errors),
                    f"scenario-count mutant survived; errors={errors}",
                )
                scenario.write_bytes(scenario_bytes)
                self.assertEqual([], validator.validate())

                readme = sandbox / "README.md"
                readme_original = readme.read_text(encoding="utf-8")
                readme.write_text(
                    readme_original + "\n<!-- harmless validator negative control -->\n",
                    encoding="utf-8",
                )
                self.assertEqual(
                    [],
                    validator.validate(),
                    "harmless documentation change must not trip structural validation",
                )
            finally:
                validator.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
