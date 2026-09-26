# Performance

Performance is a first-class engineering concern on every issue. Always perform a performance-impact triage, then measure only where the changed surface can plausibly affect latency, throughput, resource use, scalability, responsiveness, or build/runtime cost.

## Performance-impact triage

Before editing, classify the issue as `none`, `low`, `moderate`, or `high` performance impact and record the evidence/rationale. Reassess after the diff exists.

Consider at least these generic surfaces when applicable:

- algorithmic complexity and work amplification;
- database/storage query count, scan size, indexes, transactions, batching, and N+1 patterns;
- network round trips, payload size, serialization, compression, and remote dependency latency;
- memory allocation/retention, leaks, file descriptors, connections, threads/tasks, and other bounded resources;
- concurrency, contention, locks, queues, retries, backpressure, and rate limiting;
- caching behavior, invalidation, cache-key cardinality, and stampede risks;
- startup, build, compile/package, test, deployment, and cold-start cost;
- frontend/client responsiveness, rendering work, asset/bundle weight, and repeated requests where applicable;
- background/batch processing throughput and scheduling;
- scale-sensitive loops, pagination, fan-out, and unbounded collections;
- logging/telemetry volume and high-frequency instrumentation.

This is a semantic risk model, not a technology list.

## Performance implementation rules

1. Preserve established performance budgets, SLOs, SLIs, limits, and capacity assumptions when evidence exists.
2. Do not invent numeric thresholds when the project has none.
3. Prefer measurement over intuition on performance-sensitive changes.
4. Compare before/after under materially equivalent conditions when feasible.
5. Keep benchmark data, workload shape, environment, warmup, sample count, and known noise factors explicit enough to interpret results.
6. Avoid premature optimization on changes with no plausible performance impact.
7. Do not trade correctness, security, or data integrity for speed without an explicit project requirement and human-approved risk decision.
8. Do not run destructive or high-load tests against production/shared systems without explicit authorization.

## Performance validation

Depending on the risk and available project mechanisms, applicable categories may include:

- focused benchmark/microbenchmark;
- representative benchmark against an existing baseline;
- load/throughput test;
- stress/capacity-limit test;
- spike/burst test;
- soak/endurance/leak test;
- scalability test across workload size or concurrency;
- concurrency/lock/contention test;
- resource profiling/measurement;
- startup/build/package-size or client responsiveness checks;
- database/query-plan or I/O verification;
- regression comparison with historical/project budgets.

Use commands/tools discovered from the repository/Profile. Do not install a new benchmark/load-testing framework silently.

## Performance blockers

If a change violates an established project performance budget or introduces a material measured regression in a performance-sensitive path, it blocks `In Review` until fixed or a human explicitly accepts the specific regression.

When no trustworthy baseline exists, report that limitation. A single noisy measurement must not be presented as a definitive regression or improvement.
