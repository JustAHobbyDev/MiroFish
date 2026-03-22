# Mixed Bounded Entity Filing Support V1 Assessment

## Facts
1. `5` real-only bounded entities were evaluated against the new filing-evidence layer.
2. `4` entities now have direct filing support:
   - `Hitachi Energy`
   - `GE Vernova`
   - `Mitsubishi Electric`
   - `Eaton`
3. `Westrafo` remains unsupported in this lane because it is on the private-company route.

## Ranking Effect
1. `Hitachi Energy`
   - strongest overall filing-backed support by volume
2. `GE Vernova`
   - strongest component-specific support
3. `Mitsubishi Electric`
   - clear component-specific support
4. `Eaton`
   - strong backlog and capacity support
5. `Westrafo`
   - no public filing support by design

## Outcome
The bounded entity queue is now backed by:
1. source-diverse upstream evidence
2. live issuer resolution
3. collected filing documents
4. deterministic filing-evidence attachment

That is the first point in the workflow where bounded entities have real downstream filing support instead of only upstream discovery support.
