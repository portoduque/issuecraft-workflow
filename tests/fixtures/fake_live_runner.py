#!/usr/bin/env python3
"""Deterministic runner-adapter fixture used only by repository tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path


request = json.loads(sys.stdin.read())
workspace = Path(request["workspace"])
scenario = request["scenario"]

if scenario["id"] == "human-done-gate":
    (workspace / "message.txt").write_text("hello world\n", encoding="utf-8")
elif scenario["id"] == "learning-persistence-gate":
    (workspace / "note.txt").write_text("reviewed\n", encoding="utf-8")
else:
    raise SystemExit(f"unsupported fake scenario: {scenario['id']}")

transcript = []
for turn in scenario["turns"]:
    transcript.append(
        {
            "turn_id": turn["id"],
            "response": f"handled {turn['id']}",
        }
    )

print(
    json.dumps(
        {
            "transcript": transcript,
            "metadata": {
                "fake": True,
                "workflow_present": (
                    workspace / ".implement-issue/system/core/WORKFLOW.md"
                ).is_file(),
            },
            "usage": {"fixture_calls": len(transcript)},
            "cost_usd": 0,
        }
    )
)
