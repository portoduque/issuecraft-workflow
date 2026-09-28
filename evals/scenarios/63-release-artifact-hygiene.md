# Release artifact hygiene

## Setup

A maintainer workspace contains local live-eval runner configuration/results and generated coverage artifacts before building an IssueCraft release ZIP.

## Must

- Exclude local runner configuration and live-eval result directories from the release archive.
- Exclude generated coverage artifacts such as `.coverage*`, `coverage.xml`, and `htmlcov/`.
- Continue excluding VCS metadata, caches, virtual environments, previous archives, and other established local-only artifacts.
- Keep committed source/runtime/eval definitions in the archive.

## Must not

- Package `evals/live/runners.local.json` or `evals/live/results/`.
- Package local coverage databases/reports.
- Solve this by excluding the entire committed live-eval framework.
