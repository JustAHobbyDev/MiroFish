# Bounded Entity Route Priority v1

Purpose:
- rank bounded follow-up entities using route-aware support
- let private-company names compete with public names without pretending they have filing support

Rules:
1. Public supported names rank with `advance_with_public_filing_weight`.
2. Private supported names rank with `advance_with_private_company_weight`.
3. Planned private names rank below supported names and keep `collect_private_company_diligence`.
4. Unresolved names keep `resolve_issuer_and_collect_filing_route`.

Scoring guidance:
- public filing support gets a higher route bonus than private support
- private support still counts materially when it is strong and specific
- utility/operator rows use load, grid-response, and capex-response counts
- equipment rows use component, capacity, expansion, and financing counts

Boundary:
- this layer ranks next actions
- it does not convert private diligence into filing support

