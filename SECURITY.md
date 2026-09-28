# Security Policy

IssueCraft is instruction-first and does not require network access or credentials. The optional installer copies local files only and refuses managed destination symlinks so installation cannot intentionally write through those paths outside the target repository. Canonical runtime rules also require later `.implement-issue/` state writes to remain contained under the authorized repository and to refuse traversal or redirecting filesystem paths.

When IssueCraft is used by an agent, that agent may have powerful repository, shell, browser, connector, cloud, or tracker permissions. The canonical workflow therefore requires untrusted-input handling, least privilege, explicit production/destructive-action gates, secret protection, security/performance triage, risk-based validation, and a human-owned final Done gate.

## Reporting a vulnerability

Do not publish exploit details, credentials, sensitive repository data, or proof-of-concept attacks in a public issue.

Preferred path:

1. Open the repository's **Security** tab.
2. Use **Report a vulnerability** / private vulnerability reporting when that option is available.
3. Include the affected version, impact, reproduction conditions, and a minimal safe proof of concept.

If private vulnerability reporting is unavailable, open a public issue containing only a request for a private contact channel and no sensitive technical details.

Security policy page:
https://github.com/portoduque/issuecraft-workflow/security/policy

## Scope reminders

A workflow cannot guarantee that every external agent host or model will obey instructions perfectly. IssueCraft therefore backs important guarantees with repository invariants, deterministic contract evals, tests, explicit human gates, and least-privilege guidance rather than relying only on prompt text.
