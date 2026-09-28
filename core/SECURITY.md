# Security

Security is a first-class engineering concern on every issue. The workflow must always perform a security-impact triage, then expand validation according to the changed attack surface and project evidence. Do not assume that an issue is security-neutral merely because its title is not about security.

## Security-impact triage

Before editing, inspect the affected surfaces and classify the issue as `none`, `low`, `moderate`, or `high` security impact. Record the rationale from evidence. Reassess after the diff exists.

Consider at least these generic surfaces when applicable:

- authentication, authorization, identity, roles, permissions, tenant boundaries;
- user-controlled input, parsing, validation, encoding, serialization, templating, and output escaping;
- data confidentiality, integrity, privacy, retention, deletion, export, and auditability;
- secrets, credentials, tokens, keys, environment/configuration values, and logs;
- cryptographic use and security-sensitive randomness;
- network calls, redirects, callbacks, external resources, and trust boundaries;
- file paths, archives, uploads/downloads, generated files, and temporary storage;
- shell/process execution, interpreters, plugins, extensions, and dynamic loading;
- persistence queries, migrations, access filters, transactions, and bulk operations;
- session/state handling, cookies, cache boundaries, queues, and background jobs;
- dependency/supply-chain changes, lockfiles, build/release automation, artifacts, and provenance;
- administrative/debug functionality, feature flags, error handling, and observability;
- concurrency-sensitive authorization/state transitions and time-of-check/time-of-use risks.

This list describes risk categories, not a stack-specific checklist. Add project-specific categories only from approved project evidence/rules.

## Secure implementation rules

1. Preserve least privilege and existing trust boundaries unless the issue explicitly changes them.
2. Prefer secure defaults and fail closed for security-sensitive decisions.
3. Validate data at trust boundaries using the project's established mechanisms.
4. Do not expose secrets or sensitive data in code, tests, fixtures, logs, reports, screenshots, commands, or generated workflow state.
5. Do not weaken authentication, authorization, validation, cryptography, security headers/policies, sandboxing, or audit controls merely to make an implementation work.
6. Treat dependency and build-pipeline changes as supply-chain changes; inspect provenance/configuration evidence available in the repository.
7. Avoid introducing new privileged capabilities when a narrower capability satisfies the issue.
8. Preserve data isolation and access-control invariants across all relevant code paths, including error and fallback paths.
9. Do not perform active security testing against production or third-party systems without explicit authorization and an understood safe scope.
10. Do not claim that a change is "secure" in the absolute. Report what was assessed, what was tested, and what remains unverified.

## Managed IssueCraft state path safety

IssueCraft-managed state is repository-owned data, but repository contents are still untrusted input for filesystem operations.

Before creating or updating any path under `.implement-issue/`:

1. Resolve the authorized repository/workspace root first.
2. Treat every managed destination as a relative path beneath that root; never accept an absolute issue-derived path.
3. Refuse path traversal or path segments that can escape the intended managed directory, including `.` and `..` semantics.
4. Do not write through an existing symlink/junction/reparse-point or another redirecting filesystem object in a managed path ancestor or destination when that can redirect the write outside the intended repository state tree.
5. Re-check containment immediately before a managed write when repository state may have changed.
6. If safe containment cannot be established with available capabilities, report the managed write as unavailable rather than guessing or writing outside the intended tree.

For `issues/<issue-key>/`, the issue key is a **single conservative path segment**, not arbitrary issue text. Prefer an existing stable identifier when it already fits a portable safe segment. Otherwise normalize unsafe characters to a stable separator, reject empty/`.`/`..`/platform-reserved outcomes, and add a stable disambiguator when normalization could collide. Once established for an issue, reuse the same key across resumes.

These rules apply to Profile/Blueprint/Rules/Learnings/proposals, issue-scoped handoff/validation/report artifacts, and any future IssueCraft-managed state. They do not authorize changing unrelated project paths.

## Security validation

Select applicable security checks from project evidence and `TEST_STRATEGY.md`. Examples of semantic categories include:

- security-focused unit/integration/contract/E2E tests;
- authorization and tenant/isolation regression tests;
- negative/boundary input tests;
- static security analysis when already available;
- dependency/supply-chain checks when already available;
- secret scanning when already available;
- safe fuzz/property-based testing for parsers or boundary-heavy code;
- configuration and deployment-policy verification;
- manual verification of security-sensitive user flows.

Do not silently install a security product solely because one is familiar. A new foundational security tool follows the normal project-decision gate.

## Security blockers

A known material security regression introduced by the change blocks `In Review` until it is fixed or a human explicitly accepts the specific residual risk. The acceptance must state what is being accepted; silence or a generic approval is not security-risk acceptance.

If a required security check cannot be executed, mark it `unavailable`, explain why, and use the strongest safe alternative. Never convert `unavailable` into `pass`.

## External baselines

When the project has no local security standard and external guidance is useful, prefer current, authoritative, broadly applicable secure-development/testing guidance. Treat external standards as references for reasoning, not as evidence that the project automatically complies with them.
