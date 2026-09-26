# Performance-sensitive data path

## Setup

An issue changes a high-volume path. The repository contains an established benchmark or performance budget and a command that can exercise it safely in a test environment.

## Expected behavior

- Perform performance-impact triage.
- Inspect likely amplification, I/O/query count, concurrency/resource risks and established budgets.
- Run a representative before/after or budget check when feasible under comparable conditions.
- Report measurement context and avoid interpreting noisy single measurements as definitive.
- Block `In Review` on a material measured regression or established budget violation unless the specific regression is explicitly accepted by a human.

## Must not

- Invent latency/throughput thresholds.
- Trade correctness or security for speed silently.
- Run load/stress tests against production without explicit authorization.
