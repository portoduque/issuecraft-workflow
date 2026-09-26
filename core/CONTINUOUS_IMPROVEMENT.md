# Continuous Improvement

The workflow may learn from real use, but it must not self-modify silently.

## During execution

When a recurring friction, missed edge case, security/performance escape, missing test category, validation gap, or useful generic pattern is observed, classify it:

- `generic_workflow`: plausibly useful across unrelated stacks/projects/providers.
- `project_specific`: convention or constraint that belongs only to the target project.
- `agent_adapter`: discovery/invocation compatibility specific to an agent surface.
- `not_actionable`: insufficient evidence or one-off occurrence.

## Improvement proposal

For an actionable case, produce a proposal using `../templates/WORKFLOW_IMPROVEMENT_PROPOSAL.md` containing:

- problem;
- evidence/scenario;
- current behavior;
- proposed behavior;
- classification;
- expected benefit;
- risks/tradeoffs;
- regression/eval case;
- files that would change if approved.

## Adoption

Do not modify the canonical workflow as part of implementing an unrelated issue. Present the proposal for human review.

For project-specific improvements, do not silently place them in `PROJECT_RULES.md`; use the project-rule human gate.

For generic improvements to this repository, add/update an eval scenario before considering the change complete.

## End-of-issue retrospective

Before final completion, perform a short internal retrospective:

1. Was important project information rediscovered that should be proposed for approved project knowledge?
2. Did a defect escape because an applicable test family was omitted?
3. Did security-impact or performance-impact triage miss a relevant surface?
4. Did a human validation failure reveal a reusable workflow gap?
5. Did the agent depend on provider- or stack-specific behavior that belongs in an adapter/project rule rather than canonical core?

If no actionable evidence exists, create no proposal. Learning must remain evidence-driven rather than accumulating speculative rules.
