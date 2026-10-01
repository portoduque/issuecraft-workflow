# Live-agent evals

This directory contains optional behavioral evaluations that run IssueCraft against a real coding-agent runner in a disposable fixture repository.

They are **maintainer tooling**, not part of the installed `implement-issue` runtime. Normal IssueCraft users do not pay any context, dependency, or execution cost for this layer.

## Why this exists

Deterministic contract evals prove that the repository contains the intended rules. They do not prove that a real agent will follow those rules correctly.

Live-agent evals add a second question:

> Given the same repository state and task, does the candidate behavior actually improve or preserve correctness, safety, validation quality, scope discipline, and autonomy?

### Black-box behavioral criteria

Prefer criteria based on **externally observable repository/task outcomes** and decision behavior. Do not require the candidate to repeat canonical IssueCraft terminology, headings, or internal workflow mechanisms unless that exact representation is itself part of a public artifact contract or scenario acceptance requirement.

Deterministic contract evals own assertions that canonical rules/wording exist. Live evals should instead test whether those rules produce the intended behavior. This separation reduces teaching to the test and avoids rewarding terminology recognition when the underlying task outcome is wrong.

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

A baseline/candidate comparison is only causal evidence when **intervention isolation is verified**: the baseline must not receive IssueCraft through global/personal configuration, and the candidate must receive it only through the intended candidate path. Runner configuration records this under `isolation.verified` plus concrete `isolation.evidence`. Individual runs may remain exploratory with unverified isolation, but blind pairing refuses them.

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

Also record runner isolation honestly:

```json
"isolation": {
  "verified": true,
  "evidence": "personal/global workflow plugins and instructions disabled; IssueCraft loaded only when workflow_installed=true"
}
```

The evidence is host-specific maintainer evidence, not a universal recipe. Keep `verified: false` when the adapter cannot actually establish intervention exclusivity. The local runner file is gitignored.

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

The blind file exposes responses as `A` and `B`. The mapping is deliberately separate so the evaluator does not need to see which condition produced each result. Blind export requires verified isolation evidence for both conditions; this prevents a contaminated baseline from being presented as a clean comparison.

Use [rubric.md](rubric.md) plus each scenario's criteria. IssueCraft intentionally does not assign global numeric weights yet.

When runner metadata exposes token usage/cost, retain it as a secondary efficiency signal. Compare output usage between baseline/candidate only after correctness, evidence fidelity, safety/human gates, validation quality, and scope discipline are satisfied. Fewer tokens never compensate for a blocker or missing evidence.

For a workflow change whose primary claim is token/output/context economy, measure the whole intervention when practical: recurring instruction/context overhead plus output/tool/turn effects, not only the final answer length. Add a minimal terse control when the experiment can isolate whether the candidate rule adds value beyond a plain concision request. Keep usage bases explicit; provider/runtime-reported usage and local estimates are not interchangeable. A shorter candidate that is not net-better, or that weakens semantic/evidence fidelity, is a null/negative result rather than proof for adoption.

## Multi-turn scenarios

A scenario may contain multiple turns. A real runner adapter should preserve the native session when practical. If a host cannot resume sessions reliably, the adapter may provide the previous transcript explicitly, but it must record that limitation in result metadata.

The harness itself stays provider-neutral.

## Evaluation instrument calibration

If a future scenario adds an automated scorer, judge, heuristic, or executable oracle, calibrate the instrument before trusting model results whenever practical:

- a known-good/positive control should pass;
- a known-bad/negative control representing the targeted failure should fail;
- for an ordering judge, the deliberately worse reference should score worse than the acceptable reference;
- if the instrument cannot discriminate those controls, do not use its result as evidence for adopting a workflow rule.

Human blind review without an automated scorer does not need synthetic controls merely for ceremony.

## Null and negative results

A live eval is allowed to show that candidate and baseline are equivalent, that the candidate does not improve the targeted behavior, or that the candidate regresses another invariant. Do not tune instructions until the candidate "wins." A null/negative result is valid evidence for revising or rejecting the proposed workflow change.

## Runtime compatibility smoke tests

Real host-loading checks are valuable but are intentionally **not** part of canonical CI. They depend on external CLIs, authentication, network access, and vendor release behavior.

A runner integration may add a separate scheduled/release smoke check for its host. Such a check belongs to adapter/maintainer tooling and must not add provider-specific behavior to `core/`.
