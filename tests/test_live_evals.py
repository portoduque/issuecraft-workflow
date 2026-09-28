import importlib.util
import json
import sys
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


live = load_module("live_evals", ROOT / "scripts/run_live_evals.py")
FAKE_RUNNER = ROOT / "tests/fixtures/fake_live_runner.py"


class LiveEvalTests(unittest.TestCase):
    def _runner_config(self, root: Path) -> Path:
        path = root / "runners.json"
        path.write_text(
            json.dumps(
                {
                    "fake": {
                        "command": [sys.executable, str(FAKE_RUNNER)],
                        "candidate_invocation": "/implement-issue",
                        "supports_multiturn": True,
                        "timeout_seconds": 30,
                        "environment": {},
                        "isolation": {
                            "verified": True,
                            "evidence": "fake runner has no global agent/plugin state",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_committed_live_scenarios_validate(self):
        self.assertEqual([], live.validate_scenarios())
        directories = live.scenario_dirs()
        self.assertGreaterEqual(len(directories), 6)
        scenario_ids = {live.load_scenario(directory)["id"] for directory in directories}
        self.assertIn("pressure-resistance", scenario_ids)
        self.assertIn("modified-preservation", scenario_ids)
        self.assertIn("root-cause-shared-path", scenario_ids)

    def test_candidate_runs_in_disposable_fixture_and_captures_agent_diff(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = self._runner_config(root)
            output = root / "responses.jsonl"

            row = live.run_once(
                config,
                "fake",
                "human-done-gate",
                "candidate",
                1,
                output,
            )

            self.assertEqual("candidate", row["condition"])
            self.assertTrue(row["runner_metadata"]["workflow_present"])
            self.assertTrue(row["runner_isolation"]["verified"])
            paths = {item["path"] for item in row["workspace_changes"]}
            self.assertIn("message.txt", paths)
            self.assertNotIn(".implement-issue/system/core/WORKFLOW.md", paths)
            self.assertEqual(3, len(row["transcript"]))
            self.assertTrue(output.is_file())

    def test_baseline_does_not_install_issuecraft(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = self._runner_config(root)

            row = live.run_once(
                config,
                "fake",
                "learning-persistence-gate",
                "baseline",
                1,
            )

            self.assertFalse(row["runner_metadata"]["workflow_present"])
            paths = {item["path"] for item in row["workspace_changes"]}
            self.assertEqual({"note.txt"}, paths)

    def test_duplicate_capture_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = self._runner_config(root)
            output = root / "responses.jsonl"
            live.run_once(
                config,
                "fake",
                "human-done-gate",
                "baseline",
                1,
                output,
            )
            with self.assertRaises(live.LiveEvalError):
                live.run_once(
                    config,
                    "fake",
                    "human-done-gate",
                    "baseline",
                    1,
                    output,
                )

    def test_blind_export_pairs_conditions_and_separates_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = self._runner_config(root)
            output = root / "responses.jsonl"

            for condition in ("baseline", "candidate"):
                live.run_once(
                    config,
                    "fake",
                    "human-done-gate",
                    condition,
                    1,
                    output,
                )

            blind, mapping = live.blind_pairs(output)
            self.assertEqual(1, len(blind))
            self.assertEqual({"A", "B"}, set(blind[0]["responses"]))
            self.assertEqual(1, len(mapping))
            self.assertEqual(
                {"baseline", "candidate"},
                set(mapping[0]["labels"].values()),
            )
            self.assertNotIn("condition", json.dumps(blind[0]))

    def test_blind_export_rejects_unverified_isolation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = root / "runners.json"
            config.write_text(
                json.dumps(
                    {
                        "fake": {
                            "command": [sys.executable, str(FAKE_RUNNER)],
                            "candidate_invocation": "/implement-issue",
                            "supports_multiturn": True,
                            "timeout_seconds": 30,
                            "environment": {},
                            "isolation": {
                                "verified": False,
                                "evidence": "global agent state not checked",
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )
            output = root / "responses.jsonl"
            for condition in ("baseline", "candidate"):
                live.run_once(
                    config,
                    "fake",
                    "human-done-gate",
                    condition,
                    1,
                    output,
                )

            with self.assertRaisesRegex(
                live.LiveEvalError,
                "requires verified runner isolation evidence",
            ):
                live.blind_pairs(output)

    def test_verified_isolation_requires_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = root / "runners.json"
            config.write_text(
                json.dumps(
                    {
                        "fake": {
                            "command": [sys.executable, str(FAKE_RUNNER)],
                            "supports_multiturn": True,
                            "isolation": {"verified": True, "evidence": ""},
                        }
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                live.LiveEvalError,
                "verified isolation requires concrete evidence",
            ):
                live.run_once(
                    config,
                    "fake",
                    "human-done-gate",
                    "baseline",
                    1,
                )

    def test_multiturn_scenario_rejects_runner_without_multiturn_support(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = root / "runners.json"
            config.write_text(
                json.dumps(
                    {
                        "fake": {
                            "command": [sys.executable, str(FAKE_RUNNER)],
                            "supports_multiturn": False,
                        }
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(live.LiveEvalError, "supports_multiturn"):
                live.run_once(
                    config,
                    "fake",
                    "human-done-gate",
                    "baseline",
                    1,
                )


if __name__ == "__main__":
    unittest.main()
