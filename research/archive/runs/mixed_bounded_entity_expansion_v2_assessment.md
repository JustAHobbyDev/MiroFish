# Mixed Bounded Entity Expansion v2 Assessment

Date: March 21, 2026

## Facts

1. `mixed_bounded_entity_expansion_v2.json` contains `5` selected entities.
2. `v2` excludes synthetic-only entity families from the live downstream path.
3. The active real-only transformer lane now contains:
   - `Hitachi Energy`
   - `Eaton`
   - `Mitsubishi Electric`
   - `Westrafo`
   - `GE Vernova`

## Decision

1. This `v2` set replaces the earlier synthetic-contaminated live queue.
2. `GridCore Manufacturing`, `Lamina Grid Products`, `ConductorWorks`, `MeterWave Technologies`, and `Summit Compute Parks` remain available only as synthetic fixture-derived entities, not live downstream targets.

