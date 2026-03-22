# Bounded Entity Filing Priority v1

## Purpose

Deterministically reprioritize bounded entity queues after filing evidence is attached.

## Inputs

1. `bounded_entity_expansion_batch`
2. `bounded_entity_filing_support_batch`

## Output

One `priority_row` per bounded entity expansion with:

1. base priority
2. role lane
2. filing support status
3. filing evidence counts
4. role-specific evidence summary when applicable
4. filing-backed priority score
5. filing-backed priority tier
6. next action

## Scoring Intent

The priority layer should:

1. prefer entities with real filing-backed support
2. reward component-specific evidence over generic system context
3. keep unsupported entities in queue when they are still real-only and filing-eligible
4. split equipment suppliers from utilities/operators before ranking

## Role-Lane Boundary

1. `equipment_supplier`
   - rank primarily on:
     - component-specific evidence
     - capacity tightness
     - expansion or capex language
2. `utility_or_operator`
   - rank primarily on:
     - load and demand pressure
     - grid-response evidence
     - capex response evidence
3. Utilities and operators should not compete directly with equipment suppliers in one undifferentiated filing-backed queue.

## Action Boundary

1. `advance_with_filing_backed_weight`
   - entity already has usable filing support
   - downstream ranking can treat it as filing-backed

2. `resolve_and_collect_filing_route`
   - entity is still filing-eligible
   - but needs live issuer resolution and collection

3. `hold_for_additional_source_coverage`
   - entity is not yet ready for filing-led downstream work

## Current Use

This layer is intended to:

1. reprioritize the transformer/grid-equipment lane after the first filing pass
2. surface which data-center-power entities already inherit filing support through overlapping issuers
