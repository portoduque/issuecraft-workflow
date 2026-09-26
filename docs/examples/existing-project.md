# Example — Existing Project First Run

Input: `implement-issue` is invoked in an established repository with no Profile.

Expected behavior:

1. Classify as an existing project.
2. Discover repository shape and evidence.
3. Identify stack/tool facts only where evidence supports them.
4. Preserve `unknown`/`not_detected` for unresolved categories.
5. Present proposed Profile with evidence/confidence.
6. Wait for human approval before writing `PROJECT_PROFILE.yaml`.
7. After approval, resolve the issue and begin implementation.

Anti-pattern: selecting a test framework because it is conventional for the detected language when no test evidence exists.
