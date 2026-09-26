#!/usr/bin/env python3
"""Create a clean IssueCraft source ZIP.

The archive intentionally excludes VCS metadata, caches, virtual environments,
previous archives and other local-only artifacts.
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IGNORE = shutil.ignore_patterns(
    ".git",
    ".git/*",
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


def create_release_zip(output_dir: Path | None = None, source_root: Path = ROOT) -> Path:
    source_root = source_root.resolve()
    version = (source_root / "VERSION").read_text(encoding="utf-8").strip()
    output_dir = (output_dir or source_root.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_root_name = f"issuecraft-workflow-{version}"
    out_base = output_dir / archive_root_name

    with tempfile.TemporaryDirectory() as td:
        stage_root = Path(td)
        staged = stage_root / archive_root_name
        shutil.copytree(source_root, staged, ignore=IGNORE)
        archive = shutil.make_archive(
            str(out_base),
            "zip",
            root_dir=stage_root,
            base_dir=staged.name,
        )

    return Path(archive)


if __name__ == "__main__":
    print(create_release_zip())
