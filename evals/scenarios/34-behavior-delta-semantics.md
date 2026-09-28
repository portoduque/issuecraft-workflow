# Behavior delta semantics

## Setup

An issue changes externally observable behavior. Existing repository evidence establishes the current behavior, and the requested change can add, modify, remove, rename/preserve, or put nearby unchanged behavior at regression risk.

## Must

- Build a current-contract -> requested-delta -> intended-result model when it materially improves precision.
- Use repository/runtime/documentation/project-rule evidence for the current contract; do not invent a baseline.
- Treat ADDED behavior as something that must exist after the change.
- Treat REMOVED behavior as something that must no longer be delivered where removal applies.
- Treat RENAMED/PRESERVED behavior as semantically preserved without requiring unrelated internal symbol/file renames.
- Track unchanged-but-at-risk behavior as a regression obligation when the changed surface can plausibly break it.
- Prefer observable behavior/contracts over implementation-detail assertions unless the implementation choice itself is an explicit requirement.

## Must not

- Verify every delta operation as though it were a missing feature to implement.
- Re-add deliberately removed behavior because a verifier cannot find it.
- Turn an internal implementation detail chosen by the agent into a new acceptance criterion.
