# Mixed Issuer Resolution v1 Assessment

Date: March 21, 2026

## Facts

1. `mixed_issuer_resolution_v1.json` contains `6` issuer-resolution plans.
2. High-priority `resolve_first` queue:
   - `GridCore Manufacturing`
   - `Hitachi Energy`
   - `Lamina Grid Products`
3. Medium-priority `resolve_after_high` queue:
   - `Eaton`
   - `MeterWave Technologies`
   - `Westrafo`

## Route Hints

1. `Westrafo`
   - `foreign_route_hint`
   - geography hint:
     - `Italy`
2. `Eaton`
   - `domestic_route_hint`
3. `GridCore Manufacturing`
   - `route_unknown`
4. `Hitachi Energy`
   - `route_unknown`
5. `Lamina Grid Products`
   - `route_unknown`
6. `MeterWave Technologies`
   - `route_unknown`

## Decision

1. The first live issuer-resolution pass should start with the three `resolve_first` entities.
2. `Westrafo` is the clearest foreign-route case in the medium-priority set.
3. No issuer is considered resolved in `v1`; this is still a planning layer only.

