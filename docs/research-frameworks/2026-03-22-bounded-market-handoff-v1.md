# Bounded Market Handoff v1

Date: March 22, 2026

## Purpose

Create the first deterministic market-facing handoff from route-backed bounded
entity lanes.

This layer is downstream of:

1. bounded lane formation
2. public/private route support
3. route-aware priority

It is upstream of:

1. public symbol mapping
2. market research row construction
3. expression ranking

## Why This Layer Exists

The route-backed review surface is already good enough for downstream work, but
it still mixes together:

1. public names that can move into market research now
2. private names that should remain watchlist-only
3. private suppliers that should be followed through public counterparties
4. names that still need corroboration before any market-facing handoff

`bounded_market_handoff_batch_v1` makes that split explicit.

## Inputs

Primary input:

- `bounded_entity_route_review_surface_v*`

Current artifact:

- [mixed_bounded_entity_route_review_surface_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_bounded_entity_route_review_surface_v2.json)

## Output Object

Each row receives one deterministic handoff status:

1. `public_investable_now`
2. `private_watchlist_only`
3. `supplier_chain_followup`
4. `hold_for_more_corroboration`

It also receives:

1. `market_handoff_action`
2. `ticker_handoff_status`
3. `ticker_handoff_block_reason`
4. `market_expression_scope`

## Current v1 Rules

### `public_investable_now`

Requirements:

1. `support_status = supported_public_filing`
2. `route_aware_priority_tier = high`

Implication:

- eligible for public symbol mapping and market research row construction

### `supplier_chain_followup`

Requirements:

1. `support_status = supported_private_company`
2. `role_lane = equipment_supplier`

Implication:

- do not pretend there is a direct public symbol
- instead map public suppliers, customers, parents, or counterparties

### `private_watchlist_only`

Requirements:

1. `support_status = supported_private_company`
2. role is not `equipment_supplier`

Implication:

- keep the name in the bounded lane
- track private capacity and map public counterparties

### `hold_for_more_corroboration`

Used when:

1. route resolution is incomplete
2. support is planned but not collected
3. public filing support needs refresh
4. route-backed evidence is still too weak

## Important Boundary

This is still not direct ticker picking.

`public_investable_now` means:

- the entity is ready for bounded public-market mapping

It does **not** mean:

- the final ticker or expression is already chosen

## Current v1 Result

Output artifact:

- [mixed_bounded_market_handoff_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_bounded_market_handoff_v1.json)

This should turn the current narrowed lanes into:

1. public names ready for market mapping
2. private watchlist names
3. supplier-chain follow-up names

without collapsing those route types together.
