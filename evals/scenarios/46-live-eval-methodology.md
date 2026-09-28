# Live-eval methodology rigor

## Setup

Maintainers compare baseline and candidate agent behavior and may add automated evaluation instruments.

## Must

- Treat baseline/candidate comparison as causal evidence only when intervention isolation is verified and documented.
- Reject blind pairing when the runner lacks verified isolation evidence.
- Require known-good positive and known-bad negative controls for automated scorers/judges/oracles when practical before trusting their results.
- Accept null/equivalent or negative candidate results as legitimate evidence rather than tuning until the candidate wins.
- Keep secondary efficiency metrics subordinate to correctness, evidence fidelity, gates, and complete behavior.

## Must not

- Present a potentially contaminated baseline as clean causal evidence.
- Add synthetic controls to a purely human blind review when no automated instrument exists merely for ceremony.
- Adopt a workflow rule solely because it sounds plausible when evaluation demonstrates no benefit or a regression.
