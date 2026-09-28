import copy
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


installer = load_module("coverage_installer", ROOT / "scripts/install.py")
live = load_module("coverage_live", ROOT / "scripts/run_live_evals.py")
validator = load_module("coverage_validator", ROOT / "scripts/validate_repo.py")
contract = load_module("coverage_contract", ROOT / "scripts/run_evals.py")


class InstallerErrorPathTests(unittest.TestCase):
    def test_path_escape_copytree_and_update_paths(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside_td:
            target = Path(td).resolve()
            outside = Path(outside_td).resolve()
            with self.assertRaisesRegex(SystemExit, "escapes target repository"):
                installer.refuse_managed_symlinks(target, outside / "x")

            src = target / "src"
            dst = target / "dst"
            src.mkdir()
            dst.mkdir()
            (src / "new.txt").write_text("new", encoding="utf-8")
            (dst / "old.txt").write_text("old", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                installer.copytree(src, dst, overwrite=False)
            installer.copytree(src, dst, overwrite=True)
            self.assertEqual("new", (dst / "new.txt").read_text(encoding="utf-8"))
            self.assertFalse((dst / "old.txt").exists())

    def test_invalid_existing_and_overwrite_install(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            missing = root / "missing"
            with self.assertRaisesRegex(SystemExit, "does not exist"):
                installer.install(missing)

            target = root / "target"
            target.mkdir()
            installer.install(target)
            with self.assertRaisesRegex(SystemExit, "already exists"):
                installer.install(target)
            installer.install(target, overwrite_system=True)
            self.assertTrue((target / ".implement-issue/system/VERSION").is_file())

    def test_installer_main_parses_target_and_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            with mock.patch.object(installer, "install") as mocked:
                with mock.patch.object(
                    sys,
                    "argv",
                    ["install.py", str(target), "--overwrite-system"],
                ):
                    self.assertEqual(0, installer.main())
            mocked.assert_called_once_with(target, overwrite_system=True)


class LiveEvalErrorPathTests(unittest.TestCase):
    def _valid_scenario(self, scenario_id: str = "scenario"):
        return {
            "id": scenario_id,
            "description": "description",
            "risk": "low",
            "fixture": "fixture",
            "turns": [{"id": "t1", "prompt": "do it"}],
            "criteria": [{"id": "c1", "severity": "normal", "text": "works"}],
        }

    def _write_scenario(self, root: Path, scenario, fixture: bool = True) -> Path:
        directory = root / str(len(list(root.glob("case-*"))))
        directory = root / f"case-{directory.name}"
        directory.mkdir(parents=True)
        if fixture:
            (directory / "fixture").mkdir()
        (directory / "scenario.json").write_text(json.dumps(scenario), encoding="utf-8")
        return directory

    def _runner_config(self, root: Path, **overrides) -> Path:
        runner = {
            "command": ["fake-command"],
            "supports_multiturn": True,
            "timeout_seconds": 30,
            "environment": {},
            "isolation": {"verified": True, "evidence": "isolated"},
        }
        runner.update(overrides)
        path = root / "runners.json"
        path.write_text(json.dumps({"fake": runner}), encoding="utf-8")
        return path

    def test_load_scenario_rejects_malformed_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            missing = root / "missing"
            missing.mkdir()
            with self.assertRaisesRegex(live.LiveEvalError, "missing scenario.json"):
                live.load_scenario(missing)

            cases = []
            cases.append(([], True, "scenario must be an object"))

            bad = self._valid_scenario()
            bad["id"] = ""
            cases.append((bad, True, "id must be a non-empty string"))

            bad = self._valid_scenario()
            bad["turns"] = []
            cases.append((bad, True, "turns must be a non-empty list"))

            bad = self._valid_scenario()
            bad["turns"] = ["bad"]
            cases.append((bad, True, "every turn must be an object"))

            bad = self._valid_scenario()
            bad["turns"] = [{"id": "", "prompt": "x"}]
            cases.append((bad, True, "each turn needs a non-empty id"))

            bad = self._valid_scenario()
            bad["turns"] = [
                {"id": "same", "prompt": "x"},
                {"id": "same", "prompt": "y"},
            ]
            cases.append((bad, True, "duplicate turn id"))

            bad = self._valid_scenario()
            bad["turns"] = [{"id": "t", "prompt": ""}]
            cases.append((bad, True, "needs a non-empty prompt"))

            bad = self._valid_scenario()
            bad["criteria"] = []
            cases.append((bad, True, "criteria must be a non-empty list"))

            bad = self._valid_scenario()
            bad["criteria"] = ["bad"]
            cases.append((bad, True, "every criterion must be an object"))

            bad = self._valid_scenario()
            bad["criteria"] = [{"id": "", "severity": "normal", "text": "x"}]
            cases.append((bad, True, "each criterion needs an id"))

            bad = self._valid_scenario()
            bad["criteria"] = [
                {"id": "same", "severity": "normal", "text": "x"},
                {"id": "same", "severity": "normal", "text": "y"},
            ]
            cases.append((bad, True, "duplicate criterion id"))

            bad = self._valid_scenario()
            bad["criteria"] = [{"id": "c", "severity": "wrong", "text": "x"}]
            cases.append((bad, True, "invalid severity"))

            bad = self._valid_scenario()
            bad["criteria"] = [{"id": "c", "severity": "normal", "text": ""}]
            cases.append((bad, True, "needs text"))

            bad = self._valid_scenario()
            cases.append((bad, False, "fixture directory not found"))

            for index, (scenario, fixture, message) in enumerate(cases):
                with self.subTest(index=index, message=message):
                    directory = root / f"case-{index}"
                    directory.mkdir()
                    if fixture:
                        (directory / "fixture").mkdir()
                    (directory / "scenario.json").write_text(
                        json.dumps(scenario), encoding="utf-8"
                    )
                    with self.assertRaisesRegex(live.LiveEvalError, message):
                        live.load_scenario(directory)

    def test_validate_scenarios_duplicate_invalid_and_small_sets(self):
        original = live.SCENARIOS_ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                one = root / "one"
                one.mkdir()
                (one / "fixture").mkdir()
                (one / "scenario.json").write_text(
                    json.dumps(self._valid_scenario("dup")), encoding="utf-8"
                )
                live.SCENARIOS_ROOT = root
                self.assertTrue(any("at least two" in e for e in live.validate_scenarios()))

                two = root / "two"
                two.mkdir()
                (two / "fixture").mkdir()
                (two / "scenario.json").write_text(
                    json.dumps(self._valid_scenario("dup")), encoding="utf-8"
                )
                bad = root / "bad"
                bad.mkdir()
                (bad / "scenario.json").write_text("[]", encoding="utf-8")
                errors = live.validate_scenarios()
                self.assertTrue(any("duplicate live scenario id" in e for e in errors))
                self.assertTrue(any("scenario must be an object" in e for e in errors))
                with self.assertRaisesRegex(live.LiveEvalError, "unknown live scenario"):
                    live.find_scenario("missing")
        finally:
            live.SCENARIOS_ROOT = original

    def test_load_runner_rejects_invalid_configs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "runners.json"
            cases = [
                ([], "runner not found"),
                ({"fake": "bad"}, "must be an object"),
                ({"fake": {"command": []}}, "command must be"),
                ({"fake": {"command": [1]}}, "command must be"),
                ({"fake": {"command": ["x"], "timeout_seconds": True}}, "timeout_seconds"),
                ({"fake": {"command": ["x"], "timeout_seconds": 0}}, "timeout_seconds"),
                ({"fake": {"command": ["x"], "environment": []}}, "environment must map"),
                ({"fake": {"command": ["x"], "environment": {"A": 1}}}, "environment must map"),
                ({"fake": {"command": ["x"], "isolation": "bad"}}, "isolation must be an object"),
                ({"fake": {"command": ["x"], "isolation": {"verified": "yes"}}}, "verified must be boolean"),
                ({"fake": {"command": ["x"], "isolation": {"verified": False, "evidence": 1}}}, "evidence must be a string"),
            ]
            for config, message in cases:
                with self.subTest(message=message):
                    path.write_text(json.dumps(config), encoding="utf-8")
                    with self.assertRaisesRegex(live.LiveEvalError, message):
                        live.load_runner(path, "fake", 1)

    def test_snapshot_text_and_workspace_change_branches(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "keep.txt").write_text("hello", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git/secret").write_text("x", encoding="utf-8")
            (root / "__pycache__").mkdir()
            (root / "__pycache__/x.pyc").write_bytes(b"x")
            snapshot = live.snapshot_workspace(root)
            self.assertEqual({"keep.txt"}, set(snapshot))

        self.assertIsNone(live._text_or_none(b"x" * 65537))
        self.assertIsNone(live._text_or_none(b"\xff"))
        self.assertEqual("ok", live._text_or_none(b"ok"))

        changes = live.workspace_changes(
            {"same": b"x", "deleted": b"old", "modified": b"old", "binary": b"\xff"},
            {"same": b"x", "added": b"new", "modified": b"new", "binary": b"\xfe"},
        )
        by_path = {item["path"]: item for item in changes}
        self.assertEqual("added", by_path["added"]["status"])
        self.assertEqual("deleted", by_path["deleted"]["status"])
        self.assertEqual("modified", by_path["modified"]["status"])
        self.assertIn("diff", by_path["modified"])
        self.assertNotIn("diff", by_path["binary"])

    def test_jsonl_error_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            missing = root / "missing.jsonl"
            self.assertEqual(set(), live._existing_keys(missing))

            bad = root / "bad.jsonl"
            bad.write_text("\nnot-json\n", encoding="utf-8")
            with self.assertRaisesRegex(live.LiveEvalError, "invalid row"):
                live._existing_keys(bad)
            with self.assertRaisesRegex(live.LiveEvalError, "invalid JSONL row"):
                live.read_rows(bad)

            scalar = root / "scalar.jsonl"
            scalar.write_text("[]\n", encoding="utf-8")
            with self.assertRaisesRegex(live.LiveEvalError, "must be an object"):
                live.read_rows(scalar)

    def test_blind_pair_shape_errors(self):
        isolation = {"verified": True, "evidence": "isolated"}
        base = {
            "scenario_id": "s",
            "trial": 1,
            "runner": "r",
            "condition": "baseline",
            "runner_isolation": isolation,
            "description": "d",
            "risk": "low",
            "criteria": [],
            "transcript": [],
            "workspace_changes": [],
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "rows.jsonl"

            bad_condition = dict(base, condition="other")
            live.write_jsonl(path, [bad_condition])
            with self.assertRaisesRegex(live.LiveEvalError, "unexpected condition"):
                live.blind_pairs(path)

            live.write_jsonl(path, [base, dict(base)])
            with self.assertRaisesRegex(live.LiveEvalError, "duplicate result"):
                live.blind_pairs(path)

            live.write_jsonl(path, [base])
            with self.assertRaisesRegex(live.LiveEvalError, "requires baseline and candidate"):
                live.blind_pairs(path)

    def test_run_once_argument_and_runner_response_errors(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = self._runner_config(root)
            with self.assertRaisesRegex(live.LiveEvalError, "condition must be"):
                live.run_once(config, "fake", "learning-persistence-gate", "wrong", 1)
            with self.assertRaisesRegex(live.LiveEvalError, "trial must be"):
                live.run_once(config, "fake", "learning-persistence-gate", "baseline", 0)

            _, scenario = live.find_scenario("learning-persistence-gate")
            turn_ids = [turn["id"] for turn in scenario["turns"]]
            valid = [{"turn_id": turn_id, "response": "ok"} for turn_id in turn_ids]

            cases = [
                (subprocess.CompletedProcess([], 2, stdout="", stderr="boom"), "runner fake failed"),
                (subprocess.CompletedProcess([], 0, stdout="not-json", stderr=""), "returned invalid JSON"),
                (subprocess.CompletedProcess([], 0, stdout="[]", stderr=""), "response must be an object"),
                (subprocess.CompletedProcess([], 0, stdout=json.dumps({"transcript": []}), stderr=""), "transcript must contain"),
                (subprocess.CompletedProcess([], 0, stdout=json.dumps({"transcript": ["bad"] * len(turn_ids)}), stderr=""), "every transcript item"),
                (subprocess.CompletedProcess([], 0, stdout=json.dumps({"transcript": [{"turn_id": t, "response": 1} for t in turn_ids]}), stderr=""), "string turn_id and response"),
                (subprocess.CompletedProcess([], 0, stdout=json.dumps({"transcript": list(reversed(valid))}), stderr=""), "turn order mismatch"),
            ]
            for completed, message in cases:
                with self.subTest(message=message):
                    with mock.patch.object(live.subprocess, "run", return_value=completed):
                        with self.assertRaisesRegex(live.LiveEvalError, message):
                            live.run_once(
                                config,
                                "fake",
                                "learning-persistence-gate",
                                "baseline",
                                1,
                            )

            timeout_config = self._runner_config(root, timeout_seconds=1)
            with mock.patch.object(
                live.subprocess,
                "run",
                side_effect=subprocess.TimeoutExpired(cmd="fake", timeout=1),
            ):
                with self.assertRaisesRegex(live.LiveEvalError, "timed out"):
                    live.run_once(
                        timeout_config,
                        "fake",
                        "learning-persistence-gate",
                        "baseline",
                        1,
                    )

    def test_live_main_validate_run_blind_and_error_paths(self):
        with mock.patch.object(live, "validate_scenarios", return_value=["bad"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(1, live.main(["validate"]))

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / "out.jsonl"
            config = root / "runners.json"
            config.write_text("{}", encoding="utf-8")
            fake_row = {
                "scenario_id": "s",
                "trial": 1,
                "condition": "baseline",
                "runner": "fake",
            }
            with mock.patch.object(live, "run_once", return_value=fake_row):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(
                        0,
                        live.main(
                            [
                                "run",
                                "--runner-config",
                                str(config),
                                "--runner",
                                "fake",
                                "--scenario",
                                "s",
                                "--condition",
                                "baseline",
                                "--output",
                                str(output),
                            ]
                        ),
                    )

            blind_output = root / "blind.jsonl"
            mapping = root / "mapping.json"
            with mock.patch.object(live, "blind_pairs", return_value=([{"x": 1}], [{"m": 1}])):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(
                        0,
                        live.main(
                            [
                                "blind",
                                "--responses",
                                str(output),
                                "--output",
                                str(blind_output),
                                "--mapping",
                                str(mapping),
                            ]
                        ),
                    )
            self.assertTrue(blind_output.is_file())
            self.assertTrue(mapping.is_file())

            with mock.patch.object(live, "run_once", side_effect=live.LiveEvalError("boom")):
                with redirect_stderr(io.StringIO()):
                    self.assertEqual(
                        1,
                        live.main(
                            [
                                "run",
                                "--runner-config",
                                str(config),
                                "--runner",
                                "fake",
                                "--scenario",
                                "s",
                                "--condition",
                                "baseline",
                                "--output",
                                str(output),
                            ]
                        ),
                    )


class ContractEvalErrorPathTests(unittest.TestCase):
    def test_require_neutrality_run_and_main_error_paths(self):
        with self.assertRaises(AssertionError):
            contract.require("present", "missing")

        original_core = contract.CORE
        try:
            with tempfile.TemporaryDirectory() as td:
                core = Path(td)
                (core / "x.md").write_text("Codex", encoding="utf-8")
                contract.CORE = core
                with self.assertRaisesRegex(AssertionError, "provider term"):
                    contract.eval_agent_neutrality()
                (core / "x.md").write_text("Python", encoding="utf-8")
                with self.assertRaisesRegex(AssertionError, "stack term"):
                    contract.eval_stack_neutrality()
        finally:
            contract.CORE = original_core

        original_scenarios = contract.SCENARIOS
        try:
            with tempfile.TemporaryDirectory() as td:
                contract.SCENARIOS = Path(td)
                self.assertTrue(any("scenario set mismatch" in e for e in contract.run()))
        finally:
            contract.SCENARIOS = original_scenarios

        original = contract.EVALS[0]
        try:
            def boom():
                raise RuntimeError("boom")
            contract.EVALS[0] = boom
            self.assertTrue(any("01-existing-project.md" in e for e in contract.run()))
        finally:
            contract.EVALS[0] = original

        with mock.patch.object(contract, "run", return_value=["boom"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(1, contract.main())


class ValidatorErrorPathTests(unittest.TestCase):
    def test_validator_error_branches(self):
        with tempfile.TemporaryDirectory() as td:
            sandbox = Path(td) / "repo"
            shutil.copytree(
                ROOT,
                sandbox,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".coverage*"),
            )
            original_root = validator.ROOT
            validator.ROOT = sandbox
            try:
                def mutate(rel, old, new, check, needle):
                    path = sandbox / rel
                    original = path.read_text(encoding="utf-8")
                    self.assertIn(old, original, rel)
                    path.write_text(original.replace(old, new, 1), encoding="utf-8")
                    errors = []
                    check(errors)
                    self.assertTrue(
                        any(needle.lower() in error.lower() for error in errors),
                        f"{rel}: expected {needle}; errors={errors}",
                    )
                    path.write_text(original, encoding="utf-8")

                required = sandbox / "docs/testing.md"
                required_bytes = required.read_bytes()
                required.unlink()
                errors = []
                validator.check_required(errors)
                self.assertTrue(any("missing required file" in e for e in errors))
                required.write_bytes(required_bytes)

                schema = sandbox / "schemas/project-blueprint.schema.json"
                schema_original = schema.read_text(encoding="utf-8")
                schema.write_text("{", encoding="utf-8")
                errors = []
                validator.check_json(errors)
                self.assertTrue(any("invalid JSON" in e for e in errors))
                schema.write_text(schema_original, encoding="utf-8")

                self.assertEqual({}, validator.parse_frontmatter("plain"))
                self.assertEqual({}, validator.parse_frontmatter("---\nname: x"))
                self.assertEqual({"name": "x"}, validator.parse_frontmatter("---\nignored\nname: x\n---\n"))

                mutate(
                    ".agents/skills/implement-issue/SKILL.md",
                    "name: implement-issue",
                    "name: wrong",
                    validator.check_skills,
                    "invalid/missing skill name",
                )
                mutate(
                    ".agents/skills/implement-issue/SKILL.md",
                    "description:",
                    "summary:",
                    validator.check_skills,
                    "missing skill description",
                )
                mutate(
                    ".agents/skills/implement-issue/SKILL.md",
                    "core/WORKFLOW.md",
                    "core/MISSING.md",
                    validator.check_skills,
                    "does not delegate",
                )
                mutate(
                    ".agents/skills/implement-issue/SKILL.md",
                    "# Implement Issue",
                    "# Different Adapter",
                    validator.check_skills,
                    "behaviorally identical",
                )

                mutate(
                    "core/WORKFLOW.md",
                    "# Implement Issue Workflow",
                    "# Implement Issue Workflow\nCodex",
                    validator.check_core_neutrality,
                    "provider term",
                )
                mutate(
                    "core/WORKFLOW.md",
                    "# Implement Issue Workflow",
                    "# Implement Issue Workflow\nPython",
                    validator.check_core_neutrality,
                    "stack-specific term",
                )

                quality_mutants = [
                    ("core/WORKFLOW.md", "TEST_STRATEGY.md", "TEST_PLAN.md", "workflow quality contract"),
                    ("core/TEST_STRATEGY.md", "Unit", "Small-test", "test taxonomy missing"),
                    ("core/SECURITY.md", "material security regression", "security regression", "security blocker contract"),
                    ("core/PERFORMANCE.md", "performance budget", "performance target", "performance budget contract"),
                    ("core/WORKFLOW.md", "Compress presentation, never evidence", "Compact output", "output efficiency contract"),
                    ("core/VALIDATION.md", "Preserve complete validation evidence", "Keep evidence", "validation output-efficiency"),
                    ("core/WORKFLOW.md", "Retrieve context progressively", "Retrieve context", "workflow evidence-efficiency"),
                    ("core/TEST_STRATEGY.md", "Behavior-to-evidence traceability", "Test traceability", "test evidence-quality"),
                    ("core/VALIDATION.md", "Evidence-backed diff review", "Diff review", "diff-review contract"),
                    ("core/WORKFLOW.md", "Version-aware authoritative-source verification", "Source verification", "workflow v0.7"),
                    ("core/VALIDATION.md", "Validation cadence and evidence freshness", "Validation cadence", "validation v0.7"),
                    ("core/TEST_STRATEGY.md", "Behavior-delta test semantics", "Delta tests", "test v0.9 delta"),
                    ("core/EVIDENCE_MODEL.md", "Partial evidence", "Subset evidence", "evidence v0.9"),
                    ("core/HUMAN_GATES.md", "Gate H — material issue intent/scope drift", "Gate H — scope", "human-gate v0.9"),
                    ("core/ISSUE_LIFECYCLE.md", "intent and scope identity", "scope identity", "lifecycle v0.9"),
                    ("core/VALIDATION.md", "preserve material semantic qualifiers", "preserve qualifiers", "validation v0.12"),
                    ("core/PROJECT_DISCOVERY.md", "project rules, architecture and domain language", "project rules and architecture", "discovery v0.13"),
                    ("templates/PROJECT_RULES.md", "Domain vocabulary sources", "Vocabulary", "project-rules v0.13"),
                    ("core/TEST_STRATEGY.md", "strongest feasible diagnostic feedback signal", "diagnostic signal", "test v0.13"),
                    ("core/PROJECT_DISCOVERY.md", "code-coverage tooling/policy", "coverage policy", "discovery v0.14"),
                    ("core/WORKFLOW.md", "approval scope integrity", "approval integrity", "workflow v0.11"),
                    ("core/VALIDATION.md", "Approval freshness for gated actions", "Approval freshness", "validation v0.11"),
                ]
                for rel, old, new, needle in quality_mutants:
                    with self.subTest(rel=rel, old=old):
                        mutate(rel, old, new, validator.check_quality_contracts, needle)

                mutate(
                    "core/CONTINUOUS_IMPROVEMENT.md",
                    ".implement-issue/proposals/",
                    ".implement-issue/ideas/",
                    validator.check_learning_contract,
                    "persistent learning contract",
                )
                mutate(
                    "core/CONTINUOUS_IMPROVEMENT.md",
                    "Generic-change admission check",
                    "Change admission",
                    validator.check_learning_contract,
                    "anti-bloat learning contract",
                )
                mutate(
                    "core/HUMAN_GATES.md",
                    "Persistence and adoption are distinct decisions",
                    "Persistence may imply adoption",
                    validator.check_learning_contract,
                    "must separate learning persistence",
                )

                mutate(
                    "core/HUMAN_GATES.md",
                    "PROJECT_PROFILE",
                    "PROJECT_STATE",
                    validator.check_human_gates,
                    "human gate contract",
                )

                mutate(
                    "manifest.json",
                    '"name": "issuecraft-workflow"',
                    '"name": "wrong"',
                    validator.check_manifest,
                    "manifest name",
                )
                mutate(
                    "manifest.json",
                    '"canonical_entry": "core/WORKFLOW.md"',
                    '"canonical_entry": "core/OTHER.md"',
                    validator.check_manifest,
                    "canonical_entry",
                )

                mutate(
                    "README.md",
                    "IssueCraft Workflow",
                    "Workflow",
                    validator.check_readmes,
                    "onboarding missing",
                )
                readme = sandbox / "README.md"
                readme_original = readme.read_text(encoding="utf-8")
                readme.write_text(readme_original + "\n" * 100 + "<REPOSITORY_URL>\n", encoding="utf-8")
                errors = []
                validator.check_readmes(errors)
                self.assertTrue(any("too long" in e for e in errors))
                self.assertTrue(any("placeholder" in e for e in errors))
                readme.write_text(readme_original, encoding="utf-8")

                mutate(
                    "docs/project-files.md",
                    "proposals/",
                    "ideas/",
                    validator.check_documentation_integrity,
                    "missing canonical proposals",
                )
                mutate(
                    "docs/compatibility-release.md",
                    "structural adapter check",
                    "structure check",
                    validator.check_documentation_integrity,
                    "compatibility release docs",
                )
                mutate(
                    "templates/PROJECT_PROFILE.yaml",
                    "coverage_policy:",
                    "coverage_info:",
                    validator.check_documentation_integrity,
                    "template missing coverage",
                )

                schema_path = sandbox / "schemas/project-profile.schema.json"
                schema_obj = json.loads(schema_path.read_text(encoding="utf-8"))
                schema_original = json.dumps(schema_obj, indent=2) + "\n"
                del schema_obj["properties"]["observed"]["properties"]["coverage_policy"]
                schema_path.write_text(json.dumps(schema_obj, indent=2) + "\n", encoding="utf-8")
                errors = []
                validator.check_documentation_integrity(errors)
                self.assertTrue(any("schema missing observed.coverage_policy" in e for e in errors))
                schema_path.write_text(schema_original, encoding="utf-8")

                ci_mutants = [
                    ("ubuntu-latest", "ubuntu-removed", "CI matrix missing OS"),
                    ("persist-credentials: false", "persist-credentials: true", "checkout must disable"),
                    ("python scripts/run_evals.py", "python scripts/no_evals.py", "deterministic contract evals"),
                    ("python scripts/run_live_evals.py validate", "python scripts/run_live_evals.py other", "live-agent eval scenarios"),
                    ("--fail-under=90", "--fail-under=89", "CI coverage gate"),
                ]
                for old, new, needle in ci_mutants:
                    with self.subTest(ci=old):
                        mutate(".github/workflows/ci.yml", old, new, validator.check_ci_hardening, needle)

                mutate(
                    "requirements-dev.txt",
                    "coverage==7.16.1",
                    "coverage==7.16.0",
                    validator.check_ci_hardening,
                    "must stay pinned",
                )

                mutate(
                    "scripts/release_zip.py",
                    '"issuecraft-workflow-"',
                    '"artifact-"',
                    validator.check_release_hardening,
                    "artifact name",
                )

                with mock.patch.object(validator, "validate", return_value=["boom"]):
                    with redirect_stdout(io.StringIO()):
                        self.assertEqual(1, validator.main())
            finally:
                validator.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
