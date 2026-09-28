# Continuous Improvement

The workflow may learn from real use, but it must not self-modify silently. Learning, persistence, and adoption are separate steps.

## Classification

When recurring friction, a missed edge case, a security/performance escape, an omitted test family, a validation gap, or a useful reusable pattern is observed, classify it as:

- `generic_workflow`: plausibly useful across unrelated projects and agent hosts.
- `project_specific`: a convention or constraint that belongs only to the target project.
- `agent_adapter`: discovery/invocation compatibility specific to an agent surface.
- `not_actionable`: insufficient evidence or a one-off occurrence.

## Generic-change admission check

Before proposing or adopting a `generic_workflow` change, guard against append-only workflow growth:

1. **Gap** — identify the concrete missing behavior or failure.
2. **Evidence** — require a real scenario, recurring friction, failed eval, or other material evidence; novelty alone is insufficient.
3. **Overlap** — check whether an existing rule already covers the need.
4. **Merge first** — prefer strengthening/simplifying an existing rule over creating another layer, file, gate, or taxonomy item.
5. **Generality** — confirm the behavior is useful across unrelated projects/agent hosts rather than a disguised local convention.
6. **Cost** — account for context/token cost, cognitive complexity, maintenance burden, extra approvals, and new failure modes.
7. **Regression proof** — define how the change will be evaluated and how a future regression will be detected.
8. **Procedure portability** — write the generic engineering procedure, not a workaround for one model, host, version, or private tool. If the justification requires a specific agent/runtime quirk, presume the change belongs in an adapter, compatibility note, eval, or upstream bug report until a provider-neutral semantic need is demonstrated.

A proposed change should be rejected, kept project-specific/adapter-specific, or left as observation when its marginal benefit does not justify its ongoing complexity.

A useful portability test is: **could the rule still be justified without naming the model/host/tool that originally failed?** If not, it is not yet a canonical-core rule.

## Proposal

For an actionable case, prepare a proposal using `../templates/WORKFLOW_IMPROVEMENT_PROPOSAL.md`. Include:

- stable proposal identifier;
- problem;
- evidence/scenario;
- current behavior;
- proposed behavior;
- classification;
- expected benefit;
- risks/tradeoffs;
- regression/eval case;
- files or project knowledge that would change if adopted.

Preparing a proposal in the current conversation does not change future behavior.

### Recurrence strengthens evidence, not authority

The same independently grounded failure/pattern recurring across separate issues or features may strengthen the evidence for a proposal and help distinguish a reusable rule from a one-off. Record the separate grounding when it matters.

Recurrence never auto-promotes a lesson, proposal, or observation into persistent or normative behavior. Candidate/confirmed counters, frequency, or agent confidence cannot replace the human persistence/adoption gates.

## Persistence gate

Persistent learning requires explicit human approval.

After the human approves persistence, save the proposal under:

`.implement-issue/proposals/WIP-<stable-id>.md`

Do not persist rejected/speculative proposals merely to accumulate memory. Pending proposals are evidence records, not normative rules, and must not silently influence future implementation behavior.

## Learning ledger

Human-approved reusable observations may be recorded in:

`.implement-issue/LEARNINGS.md`

Use `../templates/LEARNINGS.md` when creating the ledger. Each entry records provenance, classification, status, evidence, related proposal, and adoption target.

The ledger is historical/project memory. An entry does not become normative merely because it is recorded.

## Adoption gate

Adoption is a separate explicit human decision.

- `project_specific` learning belongs in approved project knowledge such as `PROJECT_RULES.md`, `PROJECT_PROFILE.yaml`, or `PROJECT_BLUEPRINT.yaml`, using the applicable human gate.
- `generic_workflow` learning becomes a proposed change to the canonical workflow source and requires regression/eval coverage before adoption.
- `agent_adapter` learning belongs in adapter/discovery compatibility, not canonical core unless the underlying semantics are generic.

Never edit the installed canonical runtime in-place merely to apply a learning discovered while implementing an unrelated issue.

## Statuses

Use clear lifecycle states such as `proposed`, `approved_for_record`, `adopted`, `rejected`, or `superseded`. Preserve enough provenance to understand why the learning exists.

## End-of-issue retrospective

Before final completion, perform a short internal retrospective:

1. Was important project information rediscovered that should be proposed for approved project knowledge?
2. Did a defect escape because an applicable test family was omitted?
3. Did security-impact or performance-impact triage miss a relevant surface?
4. Did human validation reveal a reusable workflow gap?
5. Did the agent depend on provider- or stack-specific behavior that belongs in an adapter/project rule rather than canonical core?
6. Is there already an equivalent pending/adopted learning, making a duplicate proposal unnecessary?

If no actionable evidence exists, create no proposal. Learning must remain evidence-driven rather than accumulating speculative rules.
