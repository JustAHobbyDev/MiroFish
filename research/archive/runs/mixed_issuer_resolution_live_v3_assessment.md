# Mixed Issuer Resolution Live V3 Assessment

## Facts
1. `5` real entities were evaluated from the cleaned v2 issuer-resolution queue.
2. Public-route outcomes:
   - `Hitachi Energy -> Hitachi, Ltd.`
   - `Eaton -> Eaton Corporation plc`
   - `Mitsubishi Electric -> Mitsubishi Electric Corporation`
   - `GE Vernova -> GE Vernova Inc.`
3. Private-route outcome:
   - `Westrafo -> Westrafo S.P.A.`

## Decisions
1. `Hitachi, Ltd.` remains the first live filing-collection target because its parent route is already validated and the official filing PDFs are reachable.
2. `Eaton Corporation plc` and `GE Vernova Inc.` should use the standard U.S. public-company route:
   - official IR
   - `SEC EDGAR`
   - `10-K`
   - `10-Q`
   - `8-K`
3. `Mitsubishi Electric Corporation` should use the foreign public-company route:
   - official IR
   - Annual Securities Report
   - semi-annual securities report
4. `Westrafo S.P.A.` should not enter public filing collection because the resolved route is private-company only.

## Outcome
The live queue is now separated into:
1. public filing candidates
2. private-company diligence candidates

That prevents private entities from being pushed into the public filing path.
