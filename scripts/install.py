#!/usr/bin/env python3
"""Install the implement-issue workflow runtime into a target repository.

Uses only the Python standard library. It never creates or overwrites project-owned
PROJECT_PROFILE/PROJECT_BLUEPRINT/PROJECT_RULES files.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_COLLISION_PREFIX = "Refusing first install because an implement-issue adapter already exists"


def refuse_managed_symlinks(target: Path, path: Path) -> None:
    """Refuse to write through symlinks inside the target repository."""
    target = target.resolve()
    try:
        rel = path.relative_to(target)
    except ValueError as exc:
        raise SystemExit(f"Managed path escapes target repository: {path}") from exc

    current = target
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise SystemExit(f"Refusing to write through managed symlink: {current}")


def copytree(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists():
        if not overwrite:
            raise FileExistsError(f"destination exists: {dst}")
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def install(target: Path, overwrite_system: bool = False) -> None:
    target = target.resolve()
    if not target.exists() or not target.is_dir():
        raise SystemExit(f"Target directory does not exist: {target}")

    state = target / ".implement-issue"
    system = state / "system"
    adapters = [
        (REPO_ROOT / ".agents/skills/implement-issue", target / ".agents/skills/implement-issue"),
        (REPO_ROOT / ".claude/skills/implement-issue", target / ".claude/skills/implement-issue"),
    ]

    # Preflight every managed destination before changing the target. A first
    # install must not silently destroy an existing third-party/custom skill
    # that happens to use the same discovery path.
    refuse_managed_symlinks(target, state)
    refuse_managed_symlinks(target, system)
    for _, dst in adapters:
        refuse_managed_symlinks(target, dst.parent)
        refuse_managed_symlinks(target, dst)

    if system.exists() and not overwrite_system:
        raise SystemExit(
            f"Workflow runtime already exists at {system}. "
            "Re-run with --overwrite-system to update only runtime/adapters."
        )

    if not system.exists() and not overwrite_system:
        conflicts = [dst for _, dst in adapters if dst.exists()]
        if conflicts:
            rendered = ", ".join(str(path) for path in conflicts)
            raise SystemExit(
                f"{ADAPTER_COLLISION_PREFIX}: {rendered}. Preserve/rename the existing "
                "skill, or use --overwrite-system only when replacing it is explicitly intended."
            )

    state.mkdir(parents=True, exist_ok=True)
    if system.exists():
        shutil.rmtree(system)
    system.mkdir(parents=True)

    for name in ("core", "schemas", "templates"):
        shutil.copytree(REPO_ROOT / name, system / name)
    shutil.copy2(REPO_ROOT / "VERSION", system / "VERSION")
    shutil.copy2(REPO_ROOT / "manifest.json", system / "manifest.json")

    for src, dst in adapters:
        dst.parent.mkdir(parents=True, exist_ok=True)
        copytree(src, dst, overwrite=True)

    print(f"Installed implement-issue workflow {read_version()} into: {target}")
    print("No PROJECT_PROFILE or PROJECT_BLUEPRINT was created.")
    print("Run the skill in your coding agent; first-run onboarding will create them only after human approval.")


def read_version() -> str:
    return (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Install implement-issue into a target repository")
    parser.add_argument("target", type=Path, help="Path to the target repository/workspace")
    parser.add_argument(
        "--overwrite-system",
        action="store_true",
        help="Replace installed workflow runtime and skill adapters; preserve project-owned state",
    )
    args = parser.parse_args()
    install(args.target, overwrite_system=args.overwrite_system)
    return 0


if __name__ == "__main__":
    sys.exit(main())
