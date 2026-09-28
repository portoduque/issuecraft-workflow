# Root-cause placement

## Setup

A bug report names one symptom, but repository evidence shows sibling paths share a common invariant/enforcement point.

## Must

- Trace materially relevant callers/sibling paths when the same invariant can fail beyond the named symptom.
- Prefer the smallest common correct enforcement point when evidence shows it restores the invariant across affected paths.
- Validate the broader contract when changing a shared surface expands blast radius.
- Preserve valid existing behavior around the shared path.

## Must not

- Patch only the ticket-named caller when the same root cause remains reachable through sibling paths.
- Assume a shared location is automatically safer merely because it is shared.
- Duplicate the same guard across callers when one evidenced common enforcement point is the coherent fix.
