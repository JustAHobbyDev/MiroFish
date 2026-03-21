# Mixed Bounded Entity Expansion v1 Assessment

Date: March 21, 2026

## Facts

1. `mixed_bounded_entity_expansion_v1.json` contains `6` selected entities.
2. All `6` belong to:
   - `grid equipment and transformer buildout`
3. All `6` currently have:
   - local release or trade-press support
   - no local filing support
   - `filing_gap = true`

## Selected First Filing Expansion Set

1. `GridCore Manufacturing`
2. `Hitachi Energy`
3. `Lamina Grid Products`
4. `Eaton`
5. `MeterWave Technologies`
6. `Westrafo`

## Interpretation

1. The first downstream pass is now explicit.
2. These entities are narrow enough to justify filing-focused follow-up.
3. The limiting factor is no longer bounded-lane formation.
4. The limiting factor is source coverage, especially `company_filing`.

## Decision

1. Use these six entities as the first filing and company-source expansion set.
2. Keep:
   - `utility and large-load power`
   - `power generation and backup equipment`
   as corroboration-collection lanes, not filing-expansion lanes, until they become equally bounded.

