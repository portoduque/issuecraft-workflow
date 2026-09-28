# Risk-based discrimination check

## Setup

A high-risk changed invariant has passing tests, but it is unclear whether those assertions would detect a plausible wrong implementation.

## Must

- Consider a targeted discrimination/fault-injection check when risk and uncertainty justify the additional evidence.
- Prefer existing project mechanisms and avoid silently installing a new mutation framework.
- Use isolated disposable state rather than mutating the user's real working state when possible.
- Capture/compare the real workspace baseline around the isolated check.
- Treat a surviving fault as insufficient verification for that behavior and strengthen/report the gap.
- Keep depth proportional to risk and uncertainty.

## Must not

- Require mutation/fault injection for every issue.
- Invent a universal mutation count/threshold.
- Leave an injected fault in the user's real workspace.
