# Mixed Issuer Resolution v2 Assessment

Date: March 21, 2026

## Facts

1. `mixed_issuer_resolution_v2.json` contains `5` issuer-resolution plans.
2. All `5` are real-only downstream entities.
3. Route hints:
   - `Eaton`: `domestic_route_hint`
   - `Westrafo`: `foreign_route_hint` with `Italy`
   - `Hitachi Energy`, `Mitsubishi Electric`, `GE Vernova`: `route_unknown`

## Decision

1. This `v2` queue replaces the earlier queue that included synthetic placeholders.
2. The first fully resolved route from this cleaned queue is `Hitachi Energy -> Hitachi, Ltd. -> Hitachi IR / EDINET`.

