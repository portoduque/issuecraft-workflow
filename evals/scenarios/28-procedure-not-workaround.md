# Procedure portability over model-specific workaround

## Setup

A proposed IssueCraft core rule exists because one agent/runtime/version repeatedly mishandles a particular mechanism, but no provider-neutral engineering need has been demonstrated.

## Must

- Ask whether the rule remains justified without naming the model/host/tool that failed.
- Prefer a generic engineering procedure when there is a cross-project semantic need.
- Keep host/model/version quirks in adapters, compatibility guidance, evals, or upstream issue tracking when appropriate.
- Require generic evidence before moving a workaround into canonical core.
- Preserve the anti-bloat admission test and regression proof.

## Must not

- Encode one model's transient execution bug as a universal core rule.
- Add private tool names or provider-specific mechanics to canonical behavior when a capability-level procedure is sufficient.
- Penalize stronger/future agents with unnecessary steps that have no generic engineering justification.
