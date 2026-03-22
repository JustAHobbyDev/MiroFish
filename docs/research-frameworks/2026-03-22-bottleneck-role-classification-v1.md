# Bottleneck Role Classification v1

Date: March 22, 2026

## Purpose

Separate three different downstream meanings that had been getting conflated:

1. `bottleneck_candidate`
2. `capacity_response_operator`
3. `supply_chain_beneficiary`

This layer sits on top of:

1. route-backed review surface
2. bounded market handoff

## Why This Layer Exists

The collected companies do not all play the same role.

Some names appear to sit in potentially constrained component layers.
Some are reacting to demand pressure and capital needs.
Some are relevant suppliers or counterparties without strict bottleneck evidence.

This layer makes that distinction explicit.

## Current v1 Rules

### `capacity_response_operator`

Used when:

1. `role_lane = utility_or_operator`

Implication:

- demand pressure and capital response are present
- the company should not be treated as the bottleneck itself by default

### `bottleneck_candidate`

Used only when all of the following are true:

1. `role_lane = equipment_supplier`
2. constrained-component context is present
   - for example:
     - `transformer`
     - `grid equipment`
     - `switchgear`
     - `substation`
3. `support_strong_evidence_item_count >= 8`
4. `support_component_specific_count >= 3`
5. either:
   - `support_pressure_or_capacity_count >= 2`
   - or `support_expansion_or_capex_count >= 2`

This is intentionally strict.

### `supply_chain_beneficiary`

Used for the remaining relevant names.

That includes:

1. suppliers with relevance but without strict bottleneck evidence
2. backup-power suppliers that are important but not yet proven chokepoints
3. adjacent beneficiary names

## Important Boundary

This layer does not prove monopoly power or irreplaceability.

It only classifies the current evidence posture of each entity.

## Current Artifact

- [mixed_bottleneck_role_classification_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_bottleneck_role_classification_v1.json)
