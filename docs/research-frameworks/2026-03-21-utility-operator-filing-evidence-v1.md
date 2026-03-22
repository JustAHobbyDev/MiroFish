# Utility Operator Filing Evidence v1

## Purpose

Attach utility/operator-specific filing evidence summaries so utility parents are ranked on utility-relevant signals instead of supplier-style component counts alone.

## Applies To

1. `capacity_operator_or_owner`
2. `power_or_utility_operator`

## Summary Fields

1. `load_and_demand_signal_count`
   - counts filing evidence tied to:
     - data-center demand
     - hyperscale demand
     - load growth
     - capacity pressure
2. `grid_response_signal_count`
   - counts evidence tied to:
     - substations
     - transformers
     - switchgear
     - generation response
     - interconnection or grid-investment response
3. `capex_response_signal_count`
   - counts `expansion_or_capex` evidence items

## Intent

This summary is not a separate extraction layer.
It is a deterministic downstream interpretation of already parsed filing evidence, used only to improve ranking inside the utility/operator lane.

## Boundary

1. Equipment suppliers remain ranked primarily on component-specific evidence.
2. Utility/operator entities are allowed to rank highly on:
   - load pressure
   - grid-response need
   - capex response
3. This avoids comparing a utility parent with an equipment manufacturer using one score tuned for supplier evidence.
