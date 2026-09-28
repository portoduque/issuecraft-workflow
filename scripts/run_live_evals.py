#!/usr/bin/env python3
"""Provider-neutral live-agent evaluation harness for IssueCraft.

The harness never imports a provider SDK. A configured runner adapter receives a
single JSON request on stdin, operates in a disposable fixture workspace, and
returns one JSON response on stdout.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LIVE_ROOT = ROOT / "evals" / "live"
SCENARIOS_ROOT = LIVE_ROOT / "scenarios"

sys.path.insert(0, str(ROOT / "scripts"))
import install as installer  # noqa: E402


class LiveEvalError(RuntimeError):
    pass


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def scenario_dirs() -> list[Path]:
    return sorted(
        path.parent for path in SCENARIOS_ROOT.glob("*/scenario.json")
    )


def load_scenario(directory: Path) -> dict[str, Any]:
    path = directory / "scenario.json"
    if not path.is_file():
        raise LiveEvalError(f"missing scenario.json: {directory}")
    scenario = read_json(path)
    if not isinstance(scenario, dict):
        raise LiveEvalError(f"{path}: scenario must be an object")

    required_strings = ("id", "description", "risk", "fixture")
    for key in required_strings:
        if not isinstance(scenario.get(key), str) or not scenario[key].strip():
            raise LiveEvalError(f"{path}: {key} must be a non-empty string")

    turns = scenario.get("turns")
    if not isinstance(turns, list) or not turns:
        raise LiveEvalError(f"{path}: turns must be a non-empty list")
    seen_turns: set[str] = set()
    for turn in turns:
        if not isinstance(turn, dict):
            raise LiveEvalError(f"{path}: every turn must be an object")
        turn_id = turn.get("id")
        prompt = turn.get("prompt")
        if not isinstance(turn_id, str) or not turn_id.strip():
            raise LiveEvalError(f"{path}: each turn needs a non-empty id")
        if turn_id in seen_turns:
            raise LiveEvalError(f"{path}: duplicate turn id: {turn_id}")
        seen_turns.add(turn_id)
        if not isinstance(prompt, str) or not prompt.strip():
            raise LiveEvalError(f"{path}: turn {turn_id} needs a non-empty prompt")

    criteria = scenario.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        raise LiveEvalError(f"{path}: criteria must be a non-empty list")
    seen_criteria: set[str] = set()
    for criterion in criteria:
        if not isinstance(criterion, dict):
            raise LiveEvalError(f"{path}: every criterion must be an object")
        cid = criterion.get("id")
        severity = criterion.get("severity")
        text = criterion.get("text")
        if not isinstance(cid, str) or not cid.strip():
            raise LiveEvalError(f"{path}: each criterion needs an id")
        if cid in seen_criteria:
            raise LiveEvalError(f"{path}: duplicate criterion id: {cid}")
        seen_criteria.add(cid)
        if severity not in {"normal", "blocker"}:
            raise LiveEvalError(f"{path}: criterion {cid} has invalid severity")
        if not isinstance(text, str) or not text.strip():
            raise LiveEvalError(f"{path}: criterion {cid} needs text")

    fixture = directory / scenario["fixture"]
    if not fixture.is_dir():
        raise LiveEvalError(f"{path}: fixture directory not found: {fixture}")
    return scenario


def validate_scenarios() -> list[str]:
    errors: list[str] = []
    directories = scenario_dirs()
    if len(directories) < 2:
        errors.append("expected at least two live-agent scenarios")
    seen_ids: set[str] = set()
    for directory in directories:
        try:
            scenario = load_scenario(directory)
            scenario_id = scenario["id"]
            if scenario_id in seen_ids:
                errors.append(f"duplicate live scenario id: {scenario_id}")
            seen_ids.add(scenario_id)
        except Exception as exc:
            errors.append(str(exc))
    return errors


def find_scenario(scenario_id: str) -> tuple[Path, dict[str, Any]]:
    for directory in scenario_dirs():
        scenario = load_scenario(directory)
        if scenario["id"] == scenario_id:
            return directory, scenario
    raise LiveEvalError(f"unknown live scenario: {scenario_id}")


def load_runner(config_path: Path, runner_name: str, turn_count: int) -> dict[str, Any]:
    config = read_json(config_path)
    if not isinstance(config, dict) or runner_name not in config:
        raise LiveEvalError(f"runner not found in {config_path}: {runner_name}")
    runner = config[runner_name]
    if not isinstance(runner, dict):
        raise LiveEvalError(f"runner {runner_name} must be an object")

    command = runner.get("command")
    if (
        not isinstance(command, list)
        or not command
        or any(not isinstance(part, str) or not part for part in command)
    ):
        raise LiveEvalError(f"runner {runner_name}: command must be a non-empty string list")

    timeout = runner.get("timeout_seconds", 600)
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 3600:
        raise LiveEvalError(f"runner {runner_name}: timeout_seconds must be 1..3600")

    supports_multiturn = bool(runner.get("supports_multiturn", False))
    if turn_count > 1 and not supports_multiturn:
        raise LiveEvalError(
            f"runner {runner_name} does not declare supports_multiturn=true"
        )

    env = runner.get("environment", {})
    if not isinstance(env, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in env.items()
    ):
        raise LiveEvalError(f"runner {runner_name}: environment must map strings to strings")

    isolation = runner.get("isolation", {"verified": False, "evidence": ""})
    if not isinstance(isolation, dict):
        raise LiveEvalError(f"runner {runner_name}: isolation must be an object")
    verified = isolation.get("verified", False)
    evidence = isolation.get("evidence", "")
    if not isinstance(verified, bool):
        raise LiveEvalError(f"runner {runner_name}: isolation.verified must be boolean")
    if not isinstance(evidence, str):
        raise LiveEvalError(f"runner {runner_name}: isolation.evidence must be a string")
    if verified and not evidence.strip():
        raise LiveEvalError(
            f"runner {runner_name}: verified isolation requires concrete evidence"
        )
    return runner


def _ignored_snapshot_path(relative: Path) -> bool:
    parts = relative.parts
    return ".git" in parts or "__pycache__" in parts


def snapshot_workspace(workspace: Path) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    for path in sorted(p for p in workspace.rglob("*") if p.is_file()):
        relative = path.relative_to(workspace)
        if _ignored_snapshot_path(relative):
            continue
        snapshot[relative.as_posix()] = path.read_bytes()
    return snapshot


def _text_or_none(data: bytes) -> str | None:
    if len(data) > 65536:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def workspace_changes(before: dict[str, bytes], after: dict[str, bytes]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    for path in sorted(set(before) | set(after)):
        old = before.get(path)
        new = after.get(path)
        if old == new:
            continue
        if old is None:
            status = "added"
        elif new is None:
            status = "deleted"
        else:
            status = "modified"

        item: dict[str, Any] = {
            "path": path,
            "status": status,
            "before_sha256": hashlib.sha256(old).hexdigest() if old is not None else None,
            "after_sha256": hashlib.sha256(new).hexdigest() if new is not None else None,
        }
        old_text = _text_or_none(old or b"") if old is not None else ""
        new_text = _text_or_none(new or b"") if new is not None else ""
        if old_text is not None and new_text is not None:
            diff = "".join(
                difflib.unified_diff(
                    old_text.splitlines(keepends=True),
                    new_text.splitlines(keepends=True),
                    fromfile=f"a/{path}",
                    tofile=f"b/{path}",
                )
            )
            item["diff"] = diff
        changes.append(item)
    return changes


def _existing_keys(output: Path) -> set[tuple[str, int, str, str]]:
    if not output.exists():
        return set()
    keys: set[tuple[str, int, str, str]] = set()
    for number, line in enumerate(output.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            keys.add(
                (
                    str(row["scenario_id"]),
                    int(row["trial"]),
                    str(row["condition"]),
                    str(row["runner"]),
                )
            )
        except Exception as exc:
            raise LiveEvalError(f"{output}: invalid row {number}: {exc}") from exc
    return keys


def run_once(
    runner_config: Path,
    runner_name: str,
    scenario_id: str,
    condition: str,
    trial: int,
    output: Path | None = None,
) -> dict[str, Any]:
    if condition not in {"baseline", "candidate"}:
        raise LiveEvalError("condition must be baseline or candidate")
    if isinstance(trial, bool) or trial < 1:
        raise LiveEvalError("trial must be a positive integer")

    scenario_dir, scenario = find_scenario(scenario_id)
    runner = load_runner(runner_config, runner_name, len(scenario["turns"]))

    key = (scenario_id, trial, condition, runner_name)
    if output is not None and key in _existing_keys(output):
        raise LiveEvalError(f"result already exists for {key}")

    with tempfile.TemporaryDirectory(prefix="issuecraft-live-eval-") as td:
        workspace = Path(td) / "workspace"
        shutil.copytree(scenario_dir / scenario["fixture"], workspace)

        if condition == "candidate":
            installer.install(workspace)

        before = snapshot_workspace(workspace)
        request = {
            "protocol_version": 1,
            "action": "run_scenario",
            "condition": condition,
            "trial": trial,
            "workspace": str(workspace),
            "candidate_invocation": runner.get("candidate_invocation") if condition == "candidate" else None,
            "workflow_installed": condition == "candidate",
            "scenario": scenario,
        }

        env = os.environ.copy()
        env.update(runner.get("environment", {}))
        started = time.monotonic()
        try:
            completed = subprocess.run(
                runner["command"],
                input=json.dumps(request, ensure_ascii=False),
                text=True,
                capture_output=True,
                cwd=workspace,
                env=env,
                timeout=runner.get("timeout_seconds", 600),
                shell=False,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise LiveEvalError(
                f"runner {runner_name} timed out after {runner.get('timeout_seconds', 600)}s"
            ) from exc
        elapsed = time.monotonic() - started

        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise LiveEvalError(f"runner {runner_name} failed: {detail}")

        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise LiveEvalError(
                f"runner {runner_name} returned invalid JSON: {completed.stdout[:500]!r}"
            ) from exc
        if not isinstance(response, dict):
            raise LiveEvalError("runner response must be an object")

        transcript = response.get("transcript")
        if not isinstance(transcript, list) or len(transcript) != len(scenario["turns"]):
            raise LiveEvalError(
                f"runner transcript must contain {len(scenario['turns'])} turn(s)"
            )
        expected_turns = [turn["id"] for turn in scenario["turns"]]
        actual_turns: list[str] = []
        for item in transcript:
            if not isinstance(item, dict):
                raise LiveEvalError("every transcript item must be an object")
            turn_id = item.get("turn_id")
            response_text = item.get("response")
            if not isinstance(turn_id, str) or not isinstance(response_text, str):
                raise LiveEvalError("transcript items need string turn_id and response")
            actual_turns.append(turn_id)
        if actual_turns != expected_turns:
            raise LiveEvalError(
                f"runner transcript turn order mismatch: expected {expected_turns}, got {actual_turns}"
            )

        after = snapshot_workspace(workspace)
        row = {
            "schema_version": 1,
            "scenario_id": scenario_id,
            "description": scenario["description"],
            "risk": scenario["risk"],
            "criteria": scenario["criteria"],
            "trial": trial,
            "condition": condition,
            "runner": runner_name,
            "transcript": transcript,
            "workspace_changes": workspace_changes(before, after),
            "runner_metadata": response.get("metadata", {}),
            "runner_isolation": runner.get(
                "isolation", {"verified": False, "evidence": ""}
            ),
            "usage": response.get("usage"),
            "cost_usd": response.get("cost_usd"),
            "elapsed_seconds": round(elapsed, 3),
        }

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LiveEvalError(f"{path}: invalid JSONL row {number}") from exc
        if not isinstance(row, dict):
            raise LiveEvalError(f"{path}: row {number} must be an object")
        rows.append(row)
    return rows


def blind_pairs(responses: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, int, str], dict[str, dict[str, Any]]] = {}
    for row in read_rows(responses):
        key = (str(row["scenario_id"]), int(row["trial"]), str(row["runner"]))
        condition = str(row["condition"])
        if condition not in {"baseline", "candidate"}:
            raise LiveEvalError(f"unexpected condition in results: {condition}")
        if condition in grouped.setdefault(key, {}):
            raise LiveEvalError(f"duplicate result for {key} / {condition}")
        grouped[key][condition] = row

    blind: list[dict[str, Any]] = []
    mapping: list[dict[str, Any]] = []
    for key in sorted(grouped):
        pair = grouped[key]
        if set(pair) != {"baseline", "candidate"}:
            raise LiveEvalError(f"blind comparison requires baseline and candidate for {key}")

        for condition in ("baseline", "candidate"):
            isolation = pair[condition].get("runner_isolation", {})
            if (
                not isinstance(isolation, dict)
                or isolation.get("verified") is not True
                or not str(isolation.get("evidence", "")).strip()
            ):
                raise LiveEvalError(
                    f"blind baseline/candidate comparison requires verified runner isolation evidence for {key} / {condition}"
                )

        baseline_isolation = pair["baseline"]["runner_isolation"]
        candidate_isolation = pair["candidate"]["runner_isolation"]
        if baseline_isolation != candidate_isolation:
            raise LiveEvalError(
                "blind baseline/candidate comparison requires matching isolation "
                f"evidence for both conditions: {key}"
            )

        digest = hashlib.sha256("\x00".join(map(str, key)).encode("utf-8")).digest()
        labels = (
            {"A": "baseline", "B": "candidate"}
            if digest[0] % 2 == 0
            else {"A": "candidate", "B": "baseline"}
        )
        sample = pair["baseline"]
        blind.append(
            {
                "scenario_id": key[0],
                "trial": key[1],
                "runner": key[2],
                "description": sample.get("description"),
                "risk": sample.get("risk"),
                "criteria": sample.get("criteria"),
                "isolation_evidence": baseline_isolation.get("evidence"),
                "responses": {
                    label: {
                        "transcript": pair[condition]["transcript"],
                        "workspace_changes": pair[condition]["workspace_changes"],
                    }
                    for label, condition in labels.items()
                },
            }
        )
        mapping.append(
            {
                "scenario_id": key[0],
                "trial": key[1],
                "runner": key[2],
                "labels": labels,
            }
        )
    return blind, mapping


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="validate committed live-agent scenarios")

    run = sub.add_parser("run", help="run one scenario/condition through a runner adapter")
    run.add_argument("--runner-config", type=Path, required=True)
    run.add_argument("--runner", required=True)
    run.add_argument("--scenario", required=True)
    run.add_argument("--condition", choices=("baseline", "candidate"), required=True)
    run.add_argument("--trial", type=int, default=1)
    run.add_argument("--output", type=Path, required=True)

    blind = sub.add_parser("blind", help="export paired results under blind A/B labels")
    blind.add_argument("--responses", type=Path, required=True)
    blind.add_argument("--output", type=Path, required=True)
    blind.add_argument("--mapping", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate":
            errors = validate_scenarios()
            if errors:
                print("LIVE EVAL VALIDATION FAILED")
                for error in errors:
                    print(f"- {error}")
                return 1
            print(f"LIVE EVAL VALIDATION PASSED ({len(scenario_dirs())} scenarios)")
            return 0

        if args.command == "run":
            row = run_once(
                args.runner_config,
                args.runner,
                args.scenario,
                args.condition,
                args.trial,
                args.output,
            )
            print(
                f"captured {row['scenario_id']} trial {row['trial']} "
                f"{row['condition']} with {row['runner']}"
            )
            return 0

        blind_rows, mapping_rows = blind_pairs(args.responses)
        write_jsonl(args.output, blind_rows)
        args.mapping.parent.mkdir(parents=True, exist_ok=True)
        args.mapping.write_text(
            json.dumps(mapping_rows, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {len(blind_rows)} blind pair(s)")
        return 0
    except (LiveEvalError, OSError, json.JSONDecodeError) as exc:
        print(f"LIVE EVAL ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
