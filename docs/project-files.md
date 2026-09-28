# Project Runtime Files

After installation, the target repository receives `.implement-issue/system/` containing immutable workflow runtime material. Project-specific state is created alongside it only when appropriate.

```text
.implement-issue/
├── system/
│   ├── core/
│   ├── schemas/
│   ├── templates/
│   └── VERSION
├── PROJECT_PROFILE.yaml        # only after discovery + human approval
├── PROJECT_BLUEPRINT.yaml      # only after bootstrap + human approval
├── PROJECT_RULES.md            # optional, approved local rules
├── DISCOVERY_REPORT.md         # optional human-readable evidence snapshot
├── DRIFT_REPORT.md             # created when useful
├── proposals/                  # human-approved persisted improvement proposals
└── issues/
    └── <issue-key>/
        ├── HANDOFF.md                  # optional resume snapshot
        ├── MANUAL_VALIDATION_PLAN.md   # current issue's In Review handoff
        └── ISSUE_EXECUTION_REPORT.md   # optional issue execution/validation record
```

## Source-of-truth rules

- Runtime `system/` is the installed workflow version.
- Profile is current observed project state, not aspiration.
- Blueprint is approved intended architecture, not proof of implementation.
- Rules are local normative constraints, not generic workflow behavior.
- Issue execution artifacts are scoped under `issues/<issue-key>/`; one issue must not overwrite another issue's handoff/validation/report state.
- Validation plans may be replaced by later validation for the **same issue**, not by unrelated issues.
- Handoff is operational resume state, not project knowledge or ground truth; reconcile it against current repository/VCS/tracker/evidence before acting and replace/clear it when superseded.
- Profile, Blueprint, Rules, Learnings, and proposals remain shared project state; re-read before approved writes when concurrent modification is plausible.

## Secrets

Never store secret values in any of these files. Evidence should reference paths/keys, not credentials.
