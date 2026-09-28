# Progressive context retrieval and impact reconnaissance

## Setup

An issue targets one behavior in a large repository. Candidate files are easy to find, but the repository contains many unrelated modules and the changed surface may have callers, contracts, persistence effects, or sibling tests.

## Must

- Search broadly enough to locate candidate surfaces, then inspect highest-signal evidence first.
- Follow callers/consumers, dependencies, interfaces, data flow, analogous implementation, and related tests only when they can materially change implementation or validation.
- Track unresolved material information gaps.
- Stop retrieval once no unresolved gap can materially change scope, correctness, security, performance, compatibility, or test selection.
- Perform risk-based impact reconnaissance before editing materially coupled surfaces.
- Keep trivial isolated changes lightweight rather than forcing exhaustive dependency analysis.

## Must not

- Read the repository exhaustively just to maximize context.
- Stop at the first matching file when unresolved impact evidence could change the solution.
- Invent dependencies or impact surfaces that repository evidence does not support.
