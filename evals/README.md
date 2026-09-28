# IssueCraft Evals

IssueCraft keeps evaluation in layers so stronger behavioral testing does not make the production workflow heavier or provider-specific.

## 1. Deterministic contract evals

The files in `evals/scenarios/` are human-readable behavioral contracts.

```bash
python scripts/run_evals.py
```

The runner maps all 40 scenarios to executable assertions over the canonical repository contract. These checks require no model/API key and run in CI on every supported OS/Python matrix job.

They verify that source rules for safety, lifecycle, neutrality, drift, learning, testing, and human gates are actually present and regression-protected.

## 2. Optional live-agent evals

`evals/live/` contains a provider-neutral harness for exercising real agents in disposable fixture repositories.

This layer can compare:

- `baseline`: same task/fixture without IssueCraft installed;
- `candidate`: same task/fixture with IssueCraft installed.

The harness captures the transcript plus workspace changes, supports multi-turn scenarios through a runner-adapter protocol, and can export baseline/candidate pairs under blind labels. The modified-preservation fixture specifically exercises whether a one-member contract change preserves existing behavior that was not authorized for removal. Discipline-sensitive behaviors may also use pressure scenarios that check whether the agent preserves evidence honesty, quality controls, safety boundaries, and human gates when a prompt argues for skipping them.

Live runs are intentionally **not** required by canonical CI because they can require external agent CLIs, authentication, network access, model spend, and host-specific isolation.

See [live/README.md](live/README.md).

## Regression rule

When generic workflow behavior changes:

1. update/add the deterministic contract eval;
2. add repository tests when the invariant is machine-checkable;
3. add or update a live scenario when the change depends on actual agent behavior rather than source text alone.

When a real agent exposes a gap, capture the scenario before adopting the workflow change.
