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

Boundary:
- this is a narrowing layer, not new source collection
- it should reject generic utility suppliers and synthetic-only support
- once formed, the narrowed queue should flow through:
  - route support
  - route priority
  - route review surface

