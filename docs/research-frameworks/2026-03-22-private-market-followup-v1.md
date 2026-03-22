# Private Market Follow-Up v1

Date: March 22, 2026

## Purpose

Keep private names on a real downstream path after bounded market handoff
without pretending they have direct public symbols.

## Input

- [mixed_bounded_market_handoff_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_bounded_market_handoff_v1.json)

## Output Statuses

1. `private_supplier_chain_followup`
2. `private_capacity_watchlist_followup`

## Current Rule

### `private_supplier_chain_followup`

Used when:

1. the handoff row is private
2. the entity role lane is `equipment_supplier`

Implication:

- map public customers, suppliers, parents, and expression candidates

### `private_capacity_watchlist_followup`

Used when:

1. the handoff row is private
2. the entity role lane is `utility_or_operator`

Implication:

- track capacity, financing, and counterparties
- keep the name in the bounded market watchlist

## Current Artifact

- [mixed_private_market_followup_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_private_market_followup_v1.json)
