# Security, Performance, and Testing Baseline

The canonical workflow treats security, performance, reliability, and testing as engineering properties rather than technology-specific tools.

## Security baseline

The security contract is outcome-oriented: identify changed trust boundaries, preserve secure defaults/least privilege, protect secrets and sensitive data, validate applicable security behavior, and never claim unperformed verification. This aligns with the general secure-SDLC direction of the NIST Secure Software Development Framework (SSDF) and uses OWASP verification/testing material as useful application-security references when applicable.

Authoritative references:

- NIST Secure Software Development Framework (SSDF): https://csrc.nist.gov/projects/ssdf
- NIST SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
- OWASP Application Security Verification Standard (ASVS): https://owasp.org/projects/asvs
- OWASP Web Security Testing Guide (WSTG): https://owasp.org/projects/web-security-testing-guide

These references do **not** mean every target project is automatically compliant with a standard. Project compliance requirements must come from project evidence, documentation, or human decisions.

## Performance baseline

There is no universal latency/throughput number that is correct for every stack or product. Therefore the workflow:

1. always assesses whether a change can affect performance/resource behavior;
2. discovers project-defined budgets/SLOs/baselines when they exist;
3. measures representative before/after behavior when the risk warrants it and the environment is safe;
4. does not invent thresholds;
5. distinguishes analytical risk from measured evidence;
6. blocks known violations of established budgets unless specifically risk-accepted.

## Testing baseline

`core/TEST_STRATEGY.md` defines semantic categories rather than tools. It deliberately includes more than the common unit/integration/E2E trio because production regressions also arise at contracts, migrations, concurrency, resilience, security, performance, accessibility, compatibility, installation/upgrade, recovery, and other boundaries.

The workflow uses **comprehensive consideration + risk-based execution**:

- all categories are considered;
- relevant categories are selected from the issue/diff/risk/project evidence;
- irrelevant categories are marked `not_applicable` with rationale when recorded;
- applicable checks that cannot run are `unavailable`, never `pass`;
- existing project mechanisms are preferred;
- new foundational tooling requires the normal project-decision process.

This preserves stack neutrality while keeping validation thorough.
