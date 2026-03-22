# Public Market Research Row v1

Date: March 22, 2026

## Purpose

Build the first deterministic market-research row object for public names that
have already passed bounded market handoff.

This layer stays downstream of:

1. `public_investable_now`
2. public symbol mapping
3. bottleneck-role classification

## Why This Layer Exists

The market handoff and symbol-mapping layers answer:

1. is this name public and ready for market work?
2. do we have a reliable symbol or is follow-up still needed?

The market-research row layer answers:

1. what kind of market research row should be built?
2. is the name being treated as:
   - `bottleneck_candidate`
   - `capacity_response_operator`
   - `supply_chain_beneficiary`

## Inputs

1. public symbol mapping batches
2. bottleneck-role classification batches

## Output Statuses

1. `ready_for_market_research`
2. `symbol_followup_required_before_market_research`

## Important Boundary

This layer includes only rows that already cleared:

- `public_investable_now`

Private names do not enter this object.

## Current Artifact

- [mixed_public_market_research_rows_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_public_market_research_rows_v1.json)
