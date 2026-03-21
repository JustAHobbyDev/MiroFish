# Mixed Issuer Resolution Live v1 Assessment

Date: March 21, 2026

## Facts

1. The first live issuer-resolution pass covered `3` high-priority entities:
   - `GridCore Manufacturing`
   - `Hitachi Energy`
   - `Lamina Grid Products`
2. `GridCore Manufacturing` and `Lamina Grid Products` are not live-resolvable issuers from the current corpus.
3. Both placeholder entities are backed only by synthetic `example.com` local artifacts.
4. `Hitachi Energy` is a real operating entity.
5. Official Hitachi Energy sources state that Hitachi Energy is a wholly owned subsidiary of `Hitachi, Ltd.`

## Resolution Outcomes

### GridCore Manufacturing

1. `placeholder_not_live_resolvable`
2. reason:
   - bounded support comes from a synthetic `example.com` release artifact
3. action:
   - remove from live filing queue until replaced by a real-world bounded entity

### Hitachi Energy

1. `partially_resolved_real_entity`
2. official-company evidence supports:
   - `Hitachi Energy` is a wholly owned subsidiary of `Hitachi, Ltd.`
3. current filing-route assessment:
   - `parent_public_route_candidate`
4. action:
   - use `Hitachi, Ltd.` investor-relations and filing sources as the first live resolution route

### Lamina Grid Products

1. `placeholder_not_live_resolvable`
2. reason:
   - bounded support comes from a synthetic `example.com` release artifact
3. action:
   - remove from live filing queue until replaced by a real-world bounded entity

## Decision

1. The original three-entity `resolve_first` queue is no longer valid as a live collection queue.
2. The current live-resolvable entity from that set is:
   - `Hitachi Energy`
3. The next honest live step is:
   - resolve the `Hitachi, Ltd.` parent filing route
4. The two placeholder entities should be replaced by real-world bounded entities before any filing work continues on them.

