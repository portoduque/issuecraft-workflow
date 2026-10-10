# Root-cause placement

## Setup

A bug report names one symptom, but repository evidence shows sibling paths share a common invariant/enforcement point. Some affected behavior may also be controlled by layered, inherited, or overridden configuration/policy where the apparent shared/base value is not necessarily the effective value at the failing scope.

## Must

- Trace materially relevant callers/sibling paths when the same invariant can fail beyond the named symptom.
- Prefer the smallest common correct enforcement point when evidence shows it restores the invariant across affected paths.
- Validate the broader contract when changing a shared surface expands blast radius.
- Preserve valid existing behavior around the shared path.
- When behavior is controlled by layered/inherited/overridden configuration or policy, resolve the effective configuration at the affected scope and establish evidenced precedence before changing a shared/base layer.
- Prefer the narrowest authoritative configuration layer that matches the intended scope; change a broader/base layer only when evidence shows the invariant is genuinely shared.
- Validate materially affected sibling scopes when a broader configuration/policy layer changes.

## Must not

- Patch only the ticket-named caller when the same root cause remains reachable through sibling paths.
- Assume a shared location is automatically safer merely because it is shared.
- Duplicate the same guard across callers when one evidenced common enforcement point is the coherent fix.
- Assume the first/global/base configuration value found is the effective value for the affected scope.
- Change a broader configuration layer to fix one scoped symptom without checking precedence and sibling impact.
