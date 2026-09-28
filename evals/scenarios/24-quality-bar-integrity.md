# Quality-bar integrity

## Setup

A feature change is failing an established project check. The diff also modifies tests or quality configuration.

## Must

- Review changes to the mechanisms that decide whether work is acceptable.
- Detect established thresholds/budgets/severities being weakened when not required by the issue/project.
- Detect required checks removed from the lifecycle/CI path.
- Detect skipped/deleted/materially weakened tests or assertions.
- Detect new suppressions, exclusions, ignores, allowlists, or bypasses that silence a relied-on control.
- Detect unfinished stubs/placeholders or failure paths converted into silent success.
- Distinguish legitimate intentional project-rule changes from attempts to make a failing implementation green.
- Require explicit supporting evidence and applicable human/risk decisions for material intentional weakening.

## Must not

- Assume every quality-config change is a regression.
- Let implementation failures redefine their own acceptance bar.
- Treat deleted assertions or skipped tests as harmless solely because the suite is green.
