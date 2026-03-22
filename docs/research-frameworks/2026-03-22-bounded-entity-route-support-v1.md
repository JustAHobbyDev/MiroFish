# Bounded Entity Route Support v1

Purpose:
- attach a single support surface to bounded follow-up entities
- keep public filing support and private-company diligence support comparable
- avoid labeling private names as filing-backed

Rules:
1. Public names keep `support_route_type = public_filing`.
2. Private names keep `support_route_type = private_company`.
3. `supported_public_filing` and `supported_private_company` are both valid support states.
4. `private_company_planned` is distinct from supported.
5. Shared evidence counters use neutral names:
   - `support_evidence_item_count`
   - `support_strong_evidence_item_count`
   - `support_component_specific_count`
   - `support_pressure_or_capacity_count`
   - `support_expansion_or_capex_count`
   - `support_financing_or_capital_count`
6. Utility/operator rows may also carry role-specific summaries.

Boundary:
- this layer compares support quality across routes
- it does not erase route differences

