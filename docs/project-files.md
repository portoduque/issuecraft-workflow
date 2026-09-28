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
├── MANUAL_VALIDATION_PLAN.md   # generated for current In Review handoff
├── HANDOFF.md                  # optional resume snapshot for interrupted/incomplete work
└── improvements/               # optional proposals
```

## Source-of-truth rules

- Runtime `system/` is the installed workflow version.
- Profile is current observed project state, not aspiration.
- Blueprint is approved intended architecture, not proof of implementation.
- Rules are local normative constraints, not generic workflow behavior.
- Validation plans are issue/run artifacts and may be replaced on the next issue.
- Handoff is operational resume state, not project knowledge or ground truth; reconcile it against current repository/VCS/tracker/evidence before acting and replace/clear it when superseded.

## Secrets

Never store secret values in any of these files. Evidence should reference paths/keys, not credentials.
