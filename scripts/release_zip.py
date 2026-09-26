#!/usr/bin/env python3
"""Create a clean source ZIP for a tagged workflow release."""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
OUT_BASE = ROOT.parent / f"implement-issue-workflow-{VERSION}"

IGNORE = shutil.ignore_patterns(
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "Thumbs.db",
    ".venv",
    "venv",
    "dist",
    "*.zip",
)

with tempfile.TemporaryDirectory() as td:
    stage_root = Path(td)
    staged = stage_root / f"implement-issue-workflow-{VERSION}"
    shutil.copytree(ROOT, staged, ignore=IGNORE)
    archive = shutil.make_archive(
        str(OUT_BASE),
        "zip",
        root_dir=stage_root,
        base_dir=staged.name,
    )

print(archive)
