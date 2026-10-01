# Progressive context retrieval and impact reconnaissance

## Setup

An issue targets one behavior in a large repository. Candidate files are easy to find, but the repository contains many unrelated modules and the changed surface may have callers, contracts, persistence effects, or sibling tests. The execution environment may or may not expose semantic source-code navigation/refactoring capabilities.

## Must

- Search broadly enough to locate candidate surfaces, then inspect highest-signal evidence first.
- Prefer semantic/structural retrieval for structured source code when it materially reduces ambiguity, payload, or repeated low-signal textual reads; fall back cleanly when that capability is unavailable or unsuitable.
- When reliable diff/change-region evidence exists, prefer changed region -> enclosing semantic unit -> materially relevant relationships before broad whole-file reads, unless the whole file is the clearer/cheaper unit.
- When retrieval is bounded across multiple changed surfaces, prioritize higher-risk/high-signal surfaces while preserving enough breadth that one large surface does not silently starve material secondary surfaces.
- Make truncation, omitted regions, bounded result sets, or other partial retrieval explicit; treat them as partial evidence rather than a complete inventory.
- Follow callers/consumers, dependencies, interfaces, data flow, analogous implementation, and related tests only when they can materially change implementation or validation.
- Treat semantic relationships such as declarations, implementations, callers, and references as useful evidence rather than infallible ground truth; reconcile them with repository contracts/tests when material.
- Track unresolved material information gaps.
- Stop retrieval once no unresolved gap can materially change scope, correctness, security, performance, compatibility, or test selection.
- Perform risk-based impact reconnaissance before editing materially coupled surfaces.
- Before a structure-aware mutation, establish the current target identity/current relevant content and prefer a trustworthy structure-aware refactor when it reduces risk; otherwise use ordinary editing plus focused validation.
- Change retrieval strategy when repeated search/read activity is not closing a material information gap instead of merely reading more.
- Keep trivial isolated changes lightweight rather than forcing exhaustive dependency analysis.

## Must not

- Read the repository exhaustively just to maximize context.
- Stop at the first matching file when unresolved impact evidence could change the solution.
- Let one large or high-risk file consume the entire retrieval budget without noticing other material changed surfaces.
- Treat a truncated, capped, paginated, or otherwise partial result as proof that omitted items do not exist.
- Require semantic tooling as a prerequisite for implementation.
- Force semantic tooling onto documentation, configuration, or simple text edits where ordinary targeted retrieval is clearer.
- Assume semantic navigation/refactoring output is complete enough to replace repository evidence or required validation.
- Treat semantic diagnostics as a substitute for applicable project tests, builds, static analysis, or final review.
- Invent dependencies or impact surfaces that repository evidence does not support.
