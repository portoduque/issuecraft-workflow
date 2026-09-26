# IssueCraft Evals

The files in `evals/scenarios/` are human-readable behavioral scenarios for the canonical workflow.

IssueCraft has two eval layers:

1. **Deterministic contract evals** — `python scripts/run_evals.py` maps all 16 scenarios to executable assertions over the canonical repository contract. These run in CI on every supported OS/Python matrix job.
2. **Live-agent behavioral evals** — optional host-specific runs where a real coding agent is asked to execute a scenario in a sandbox repository.

The deterministic layer is intentionally provider-neutral and requires no model API key. It verifies that the source contract actually contains the required safety, lifecycle, neutrality, drift, learning, testing, and human-gate behavior rather than only checking that scenario Markdown files exist.

Live-agent evals are useful for measuring host/model adherence, but they must remain outside the canonical pass/fail requirement unless a neutral execution harness exists. A model-specific CI dependency would contradict the project's portability goal.

When generic workflow behavior changes, update the relevant scenario and its deterministic assertion. When a real agent exposes a gap, capture that as evidence and add regression coverage before adopting the workflow change.
