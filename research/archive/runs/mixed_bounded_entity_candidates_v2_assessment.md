# Mixed Bounded Entity Candidates v2 Assessment

Date: March 21, 2026

## Facts

1. `v2` excludes synthetic-only downstream candidates from the live path.
2. The active real-only transformer lane now uses real entities only.

## First Downstream Entity Expansion Test

Selected real-only entities:

1. `Hitachi Energy`
2. `Eaton`
3. `Mitsubishi Electric`
4. `Westrafo`
5. `GE Vernova`

## Decision

1. These five replace the synthetic-placeholder-driven set for live downstream work.
2. Synthetic-only entities remain in fixture corpora only and are excluded from live queues.

