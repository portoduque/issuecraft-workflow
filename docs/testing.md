# Testing and Coverage

IssueCraft is stack- and test-framework-neutral. The canonical rules live in `../core/TEST_STRATEGY.md`; this document explains how to apply them.

## Selection model

For every issue:

1. identify materially changed behavior, acceptance criteria and risk surfaces;
2. consider the full semantic test taxonomy;
3. select only the test/check types that can materially prove those obligations;
4. use the lowest-cost faithful layer first;
5. escalate to integration/system/E2E or runtime evidence only when the risk crosses those boundaries;
6. record `pass`, `fail`, `not_applicable` or `unavailable` with evidence.

Relevant families can include unit, component, integration, contract, API/interface, system, end-to-end, acceptance, smoke, regression, negative/boundary, state/data-integrity, property/fuzz/mutation, concurrency/resilience, security, performance/load/stress/soak, accessibility/visual/compatibility, migration/recovery, lint/type/static/build and other project-specific checks.

## Behavior evidence

A broad green suite is not enough by itself. Materially changed behavior should be tied to an assertion, observation or measurement that would distinguish the expected result from the relevant failure.

For bug fixes, prefer a durable regression reproducer when faithful and feasible. For intermittent, load-sensitive or production-only defects, the strongest signal may instead be a trace, replay, benchmark, profiler measurement or scoped instrumentation.

## Code coverage

Coverage is a quality signal and regression guard, not proof of correctness.

When the target project already has coverage support, discover:

- command/tool;
- measured scope;
- line/branch or project-specific metric;
- existing threshold/baseline;
- CI enforcement.

Then:

- execute the existing coverage check when applicable;
- preserve or improve an established threshold/baseline;
- never lower/exclude/narrow coverage merely to make the issue pass;
- directly test materially new/changed executable behavior when viable;
- do not invent a universal percentage for projects that have no policy.

If coverage tooling is absent, IssueCraft does not silently install a framework. A recurring/material gap can become a project-specific improvement proposal.

## IssueCraft repository coverage

IssueCraft itself has a repository-specific branch-aware coverage gate for Python scripts. This policy is local to IssueCraft; it is not imposed on target projects.

Install the pinned development dependency:

```bash
python -m pip install -r requirements-dev.txt
```

Run:

```bash
python -m coverage erase
python -m coverage run --branch --source=scripts -m unittest discover tests -v
python -m coverage run --append --branch --source=scripts scripts/validate_repo.py
python -m coverage run --append --branch --source=scripts scripts/run_evals.py
python -m coverage run --append --branch --source=scripts scripts/run_live_evals.py validate
python -m coverage report --show-missing --fail-under=90
```

CI enforces the same threshold in a dedicated Ubuntu/Python 3.13 job while the normal test suite remains cross-platform.
