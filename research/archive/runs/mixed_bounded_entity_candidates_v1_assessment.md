# Mixed Bounded Entity Candidates v1 Assessment

Date: March 21, 2026

## Facts

1. `mixed_bounded_entity_candidates_v1.json` contains `36` bounded entity candidates.
2. `data center power demand buildout`
   - entity candidates: `26`
3. `grid equipment and transformer buildout`
   - entity candidates: `10`

## Transformer Lane

The first downstream entity-expansion test should use:

1. `Lamina Grid Products`
2. `Hitachi Energy`
3. `GridCore Manufacturing`
4. `Eaton`
5. `Westrafo`
6. `MeterWave Technologies`

These are the cleanest first-step entities because they are:

1. inside the bounded lane
2. explicitly tied to transformer, switchgear, meter, or substation equipment
3. suitable for the next source-class expansion into filings and additional releases

## Holdouts

Keep in the bounded entity output, but do not treat as first filing-expansion targets:

1. `ConductorWorks`
2. `GE Vernova`
3. `Summit Compute Parks`

Reason:

1. they are adjacent or broader than the core transformer lane
2. they need more lane-specific corroboration before promotion

## Important Gap

The deterministic output still contains corporate-family duplication:

1. `Hitachi`
2. `Hitachi Energy`

That is acceptable in `v1`, but family normalization should be added before a larger downstream universe-expansion pass.

## Decision

1. Use the transformer lane as the first downstream entity-expansion test.
2. Start with the six entities above.
3. Keep corroboration collection focused on:
   - `utility and large-load power`
   - `power generation and backup equipment`

