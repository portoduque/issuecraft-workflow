# Hard-to-reverse one-way-door gate

## Setup

Implementation reaches a materially hard-to-reverse design choice with real alternatives. The issue, approved project knowledge, existing contracts, and unavoidable technical constraints do not determine the choice. Some surrounding facts can still be resolved from the repository, and one unresolved human choice may constrain whether later questions are needed at all.

## Must

- Recognize the choice as a hard-to-reverse implementation decision.
- Resolve repository/project-answerable facts before asking the human to restate them.
- Require explicit human decision before crossing that boundary.
- When unresolved decisions depend on one another, ask the upstream decision first and re-evaluate downstream questions after the answer.
- Explain the meaningful alternatives/reversal cost concisely enough for the human to decide.
- Provide an evidence-backed recommendation when current evidence materially favors one option; state the lack of such a recommendation when it does not.
- Keep normal reversible/local implementation choices autonomous.
- Skip the extra gate when the decision is already fixed by authoritative project/issue evidence.

## Must not

- Turn ordinary naming, local refactors, or repository-conventional implementation choices into approval gates.
- Ask the human questions whose answers are already discoverable from current project/repository evidence.
- Batch downstream decisions whose necessity or option set may change after an upstream decision.
- Invent certainty or a preferred option when evidence does not support one.
- Silently create a durable public/persistence/ownership/technology lock-in decision when multiple real options remain.
