# Project Bootstrap

Use Bootstrap when there is not enough implementation evidence to construct a truthful `PROJECT_PROFILE`.

## Principle

Do not "discover" a stack that does not exist. Capture intended decisions in `PROJECT_BLUEPRINT`; leave unresolved choices unresolved.

## Classification

### Documented but implementation-free

Read meaningful project docs/specs/ADRs first. Extract only explicit architectural/product constraints and mark them `source: documentation` with file evidence. Ask questions only for decisions that are required for the current issue and still unresolved.

### Empty/near-empty

Start an adaptive Bootstrap interview. A placeholder README, license, empty directories, VCS metadata, or workflow files do not constitute implementation evidence.

## Bootstrap interview

Ask one compact initial batch. Adapt wording to the project, but cover only what is needed to avoid inventing foundational decisions:

1. What is the project/product type and primary goal?
2. Are any languages, runtimes, frameworks, platforms, or architectural constraints already mandatory?
3. Are there deployment/runtime environment constraints already decided?
4. Is persistent storage required, and is any storage/database choice already decided?
5. Are there already-decided expectations for tests/quality/CI?
6. Are there security/privacy/compliance constraints or trust boundaries already decided?
7. Are there performance/reliability/capacity targets or budgets already decided?
8. Are there constraints from an external system, organization, API, license, hosting environment, or supported platform?
7. For undecided technology choices, should they remain undecided, or does the human want proposals/options?

Do not ask questions whose answers already exist in supplied documentation or the current conversation.

## Follow-up questions

Only ask follow-ups that are necessary for the current issue/initial scaffold. Avoid a giant architecture questionnaire. If a choice can safely remain open, record `undecided`.

If the human asks for recommendations, propose options and tradeoffs, but the selected foundational choice becomes part of the Blueprint only after human approval.

## Blueprint model

Use `../templates/PROJECT_BLUEPRINT.yaml`. Every material decision should have:

- `state`: `decided`, `undecided`, or `not_applicable`;
- `value` when decided;
- `source`: `human` or `documentation`;
- evidence/reference when documentation is the source;
- optional rationale/constraints.

A Blueprint is not evidence that the repository already implements the decision.

## Approval gate

Present the proposed Blueprint and unresolved decisions. Obtain explicit approval before writing `.implement-issue/PROJECT_BLUEPRINT.yaml`.

## From Blueprint to Profile

As implementation appears, run discovery on later executions. Build a Profile from actual repository evidence. Keep the Blueprint as intended design/history.

When Blueprint and Profile diverge, report architecture drift. Do not assume whether the implementation or the plan is wrong.
