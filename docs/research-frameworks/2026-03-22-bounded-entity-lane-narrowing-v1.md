# Bounded Entity Lane Narrowing v1

Purpose:
- form a tighter, real-only follow-up lane from an exploratory bounded lane
- do this before widening source collection
- immediately reuse the existing downstream machinery once the narrower lane exists

Current rule:
1. Start from `utility and large-load power buildout`.
2. Keep only `real_only` entity candidates.
3. Keep only rows with explicit data-center utility-response titles, such as:
   - deals
   - load growth
   - pipeline pressure
   - spending-plan response
   - campus buildout tied to utility response
4. Relabel the narrowed lane as:
   - `data center utility response buildout`

Decision:
1. This narrowed lane is in service of tracking capital flow and the supply chains affected by it.
2. Because downstream supplier mapping depends on semantic discipline, the lane stays strict.
3. Explicit `data center` linkage is required for admission into
   `data center utility response buildout`.
4. Broad utility load-growth or spending-response artifacts without explicit
   data-center linkage stay in the broader parent lane:
   - `utility and large-load power buildout`
5. Example:
   - `Southern` remains in the broader parent lane for now
   - it does not enter `data center utility response buildout` under `v1`

Deferred lane:
1. A separate narrowing candidate such as:
   - `large-load utility capex response`
   may be created later
2. That lane is explicitly deferred unless new evidence shows it is needed
   and can be bounded cleanly
3. Do not widen the current data-center lane to absorb that broader concept

Boundary:
- this is a narrowing layer, not new source collection
- it should reject generic utility suppliers and synthetic-only support
- it should also reject non-explicit large-load utility response artifacts from
  the data-center-specific lane, even when they imply real capital flow
- once formed, the narrowed queue should flow through:
  - route support
  - route priority
  - route review surface
