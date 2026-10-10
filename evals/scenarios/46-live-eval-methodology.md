# Live-eval methodology rigor

## Setup

Maintainers compare baseline and candidate agent behavior and may add automated evaluation instruments.

## Must

- Treat baseline/candidate comparison as causal evidence only when intervention isolation is verified and documented.
- Reject blind pairing when the runner lacks verified isolation evidence.
- Bind each captured result to a deterministic experiment identity derived from the scenario definition and fixture inputs that materially define the task.
- Reject blind baseline/candidate pairing when those experiment identities differ or are missing; the same scenario id/trial/runner is not sufficient evidence that the experiment stayed unchanged.
- Require known-good positive and known-bad negative controls for automated scorers/judges/oracles when practical before trusting their results.
- Accept null/equivalent or negative candidate results as legitimate evidence rather than tuning until the candidate wins.
- For observable actions or state, prefer direct workspace/tool/runtime evidence over contradictory agent self-report when such evidence is available.
- Bound every conclusion to the scenario scope actually exercised; a focused/protocol/partial-workflow pass is not full-workflow, cross-host, or release proof.
- Keep secondary efficiency metrics subordinate to correctness, evidence fidelity, gates, and complete behavior.

## Must not

- Present a potentially contaminated baseline as clean causal evidence.
- Compare a baseline captured from one scenario/fixture definition with a candidate captured after that experiment materially changed.
- Add synthetic controls to a purely human blind review when no automated instrument exists merely for ceremony.
- Accept an agent's self-report as proof of an observable action when stronger direct evidence contradicts it.
- Promote a focused/checkpoint/partial scenario pass into an end-to-end or release claim it did not exercise.
- Require a universal tool-trace schema merely to enforce evidence precedence when existing workspace/runtime evidence is sufficient.
- Adopt a workflow rule solely because it sounds plausible when evaluation demonstrates no benefit or a regression.
