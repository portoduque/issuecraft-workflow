# Agent Compatibility Release Smoke Checks

The canonical workflow stays provider-neutral. These release checks validate adapters/host compatibility without moving provider-specific behavior into `core/`.

Run this checklist for a release that changes adapters, installer behavior, skill discovery/invocation, or live-eval protocol. It is also useful periodically because external agent hosts can change independently of IssueCraft.

## Preconditions

- use disposable test repositories/workspaces;
- isolate personal/global plugins, memories and instructions as required by the live-eval methodology;
- use the released candidate runtime;
- record exact agent/host version when available;
- never use production data or credentials.

## Implicit routing smoke

When a host supports description-based/implicit skill discovery, verify routing as part of adapter/invocation changes and periodic compatibility checks:

1. Run a **positive trigger** using a natural repository task that should activate `implement-issue` without explicitly naming the skill.
2. Run a **negative adjacent prompt** that is related to code/repository work but should not activate the implementation workflow (for example, explanation-only/read-only help).
3. Record whether the host selected the skill in each case and the exact host/version tested.
4. If the host does not expose or support implicit routing, mark this check `not_applicable`; do not infer success from explicit invocation.

This is a host-compatibility smoke check, not canonical workflow behavior, and does not belong in provider-neutral `core/`.

## Required hosts

### Codex

1. Install IssueCraft into a disposable repository.
2. Confirm `.agents/skills/implement-issue/SKILL.md` is discovered.
3. Invoke `$implement-issue`.
4. Run at least one critical live scenario.
5. Record discovery/invocation result and any host-specific incompatibility.

### Claude Code

1. Install IssueCraft into a disposable repository.
2. Confirm `.claude/skills/implement-issue/SKILL.md` is discovered.
3. Invoke `/implement-issue`.
4. Run at least one critical live scenario.
5. Record discovery/invocation result and any host-specific incompatibility.

### Antigravity

1. Install IssueCraft into a disposable repository.
2. Confirm `.agents/skills/implement-issue/SKILL.md` is discovered.
3. Invoke `/implement-issue`.
4. Run at least one critical live scenario.
5. Record discovery/invocation result and any host-specific incompatibility.

## Suggested critical scenarios

Prioritize:

- first-run project discovery/bootstrap;
- human Done gate;
- learning persistence gate;
- diagnostic reset;
- modified-behavior preservation;
- root-cause shared-path behavior.

## Harness

`scripts/run_live_evals.py` is provider-neutral. Configure a runner adapter in a local copy of `evals/live/runners.example.json`, then use:

```bash
python scripts/run_live_evals.py run \
  --runner-config path/to/runners.json \
  --runner <runner-name> \
  --scenario <scenario-id> \
  --condition candidate \
  --output results.jsonl
```

The runner adapter, not canonical core, owns host-specific CLI/API details.

Do not report compatibility as verified unless the relevant host was actually exercised. A structural adapter check is useful but is not the same as a live host smoke result.
