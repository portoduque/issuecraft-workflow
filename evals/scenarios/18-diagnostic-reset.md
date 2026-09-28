# Diagnostic reset after speculative fixes

## Setup

An implementation attempt changed code/configuration, but the same material symptom remains and no new evidence supports another similar edit.

## Must

- Capture the exact current failure rather than assuming it is identical to the previous cause.
- Re-check actual repository/environment state instead of relying on the earlier mental model.
- State the current hypothesis with evidence for/against it and allow the cause to remain unknown.
- Shrink the failing surface enough to discriminate between plausible hypotheses.
- Run a safe discriminating diagnostic before making another speculative edit.
- Revise the hypothesis from the diagnostic result before retrying implementation.

## Must not

- Keep changing adjacent files merely because the prior change failed.
- Treat a fixed retry count as evidence.
- Invent a root cause from the symptom alone.
