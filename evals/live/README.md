# Live-agent evals

This directory contains optional behavioral evaluations that run IssueCraft against a real coding-agent runner in a disposable fixture repository.

They are **maintainer tooling**, not part of the installed `implement-issue` runtime. Normal IssueCraft users do not pay any context, dependency, or execution cost for this layer.

## Why this exists

Deterministic contract evals prove that the repository contains the intended rules. They do not prove that a real agent will follow those rules correctly.

Live-agent evals add a second question:

> Given the same repository state and task, does the candidate behavior actually improve or preserve correctness, safety, validation quality, scope discipline, and autonomy?

## Safety model

Live evals must never point an agent at a real project, production system, personal home directory, or repository containing secrets.

The harness:

1. copies a committed fixture into a temporary workspace;
2. installs IssueCraft only for the `candidate` condition;
3. snapshots that prepared workspace;
4. invokes an explicitly configured runner adapter without `shell=True`;
5. captures the runner transcript and post-run workspace diff;
6. deletes the temporary workspace when the run finishes.

The external runner adapter remains responsible for provider-specific isolation such as disabling personal plugins/memory/config, selecting a model, constraining network/tool access, and enforcing provider spending limits.

## Runner protocol

A runner is any executable that:

- reads one JSON request from stdin;
- operates only in the supplied `workspace`;
- handles the scenario turns, preserving conversational state when the host supports it;
- writes one JSON object to stdout.

Request shape:

```json
{
  "protocol_version": 1,
  "action": "run_scenario",
  "condition": "candidate",
  "trial": 1,
  "workspace": "/temporary/workspace",
  "candidate_invocation": "/implement-issue",
  "workflow_installed": true,
  "scenario": {
    "id": "human-done-gate",
    "turns": []
  }
}
```

Expected response shape:

```json
{
  "transcript": [
    {"turn_id": "implement", "response": "..."}
  ],
  "metadata": {
    "model": "optional",
    "host_version": "optional"
  },
  "usage": {},
  "cost_usd": null
}
```

The harness does not assume any specific model/provider response format.

## Validate scenarios

```bash
python scripts/run_live_evals.py validate
```

This is offline and runs in normal CI through repository tests.

## Configure a runner

Copy:

```bash
cp evals/live/runners.example.json evals/live/runners.local.json
```

Then point `command` at a local adapter for the agent host you want to evaluate.

The local runner file is gitignored.

## Run a condition

```bash
python scripts/run_live_evals.py run \
  --runner-config evals/live/runners.local.json \
  --runner my-runner \
  --scenario human-done-gate \
  --condition candidate \
  --trial 1 \
  --output evals/live/results/responses.jsonl
```

Run the same scenario/trial with `--condition baseline` for comparison. Each condition receives a fresh copy of the fixture. The baseline does not install IssueCraft; the candidate does.

Completed keys cannot be silently overwritten in the same output file.

## Blind a baseline/candidate pair

```bash
python scripts/run_live_evals.py blind \
  --responses evals/live/results/responses.jsonl \
  --output evals/live/results/blind.jsonl \
  --mapping evals/live/results/blind-mapping.json
```

The blind file exposes responses as `A` and `B`. The mapping is deliberately separate so the evaluator does not need to see which condition produced each result.

Use [rubric.md](rubric.md) plus each scenario's criteria. IssueCraft intentionally does not assign global numeric weights yet.

When runner metadata exposes token usage/cost, retain it as a secondary efficiency signal. Compare output usage between baseline/candidate only after correctness, evidence fidelity, safety/human gates, validation quality, and scope discipline are satisfied. Fewer tokens never compensate for a blocker or missing evidence.

## Multi-turn scenarios

A scenario may contain multiple turns. A real runner adapter should preserve the native session when practical. If a host cannot resume sessions reliably, the adapter may provide the previous transcript explicitly, but it must record that limitation in result metadata.

The harness itself stays provider-neutral.

## Runtime compatibility smoke tests

Real host-loading checks are valuable but are intentionally **not** part of canonical CI. They depend on external CLIs, authentication, network access, and vendor release behavior.

A runner integration may add a separate scheduled/release smoke check for its host. Such a check belongs to adapter/maintainer tooling and must not add provider-specific behavior to `core/`.
