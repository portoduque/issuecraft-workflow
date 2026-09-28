# Compatibility-safe migrations and cutovers

## Setup

A schema/data/interface/runtime transition must coexist with old consumers during a rollout window.

## Must

- Prefer an additive expand -> migrate/cut over -> contract sequence when coexistence is required.
- Keep old and new consumers valid for the compatibility window supported by project evidence.
- Delay destructive removal until evidence shows relevant consumers no longer depend on the old shape.
- Use the project's actual recovery strategy rather than inventing a reversible/down migration.
- Apply production/high-load authorization and performance rules to large backfills or other load-sensitive work.

## Must not

- Couple an additive introduction and destructive removal when old consumers may still run.
- Claim a migration is reversible when data/platform semantics make that false.
- Run destructive or load-heavy migration work against production/shared systems without the required authorization.
