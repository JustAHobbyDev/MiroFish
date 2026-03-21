# Energy Flow Pressure Cluster v1

Date: March 21, 2026

## Purpose

Define the first aggregation object above `energy_flow_pressure_signal`.

This object exists to preserve physically important pressure signals without
 weakening the direct capital-flow gate.

It is:

- upstream of `structural_pressure_candidate`
- downstream of `energy_flow_pressure_signal`
- focused on energy as a necessary production input

## Facts

1. Utility load-growth and interconnection-pipeline articles are often valid
   energy-pressure signals even when they are weak direct capital-flow signals.
2. Energy pressure is a different evidence lane from direct financial response.
3. Separate clustering makes it easier to see whether physical pressure is
   strong even when committed spend is still sparse.

## Definition

An `energy_flow_pressure_cluster` is a bounded grouping of compatible
`energy_flow_pressure_signal`s that suggests rising strain, load, or response
 need in an energy system tied to a concrete production or buildout story.

## Required Invariants

Every valid `energy_flow_pressure_cluster` must have:

1. `Signal plurality`
   - at least two supporting `energy_flow_pressure_signal`s
2. `Physical-system grounding`
   - the cluster names a real energy system or load corridor
3. `Pressure orientation`
   - the cluster reflects load growth, pipeline pressure, capacity tightness, or
     infrastructure-response need
4. `Explicit time boundary`
   - supporting evidence lives within a defined window
5. `Source provenance`
   - every member signal is traceable

## Minimal Shape

```json
{
  "energy_flow_pressure_cluster_id": "efpc_utility_load_2026_02_28_v1",
  "as_of_date": "2026-02-28",
  "status": "candidate",
  "system_label": "US utility and large-load power demand pressure",
  "cluster_statement": "Utility and large-load artifacts imply rising electricity demand, interconnection pressure, and infrastructure-response need tied to data-center growth.",
  "supporting_energy_flow_signal_ids": [
    "efs_021",
    "efs_033",
    "efs_047"
  ],
  "signal_count": 3,
  "source_classes": [
    "trade_press"
  ],
  "time_window": {
    "start_date": "2025-12-01",
    "end_date": "2026-02-28"
  },
  "pressure_types_present": [
    "load_growth",
    "infrastructure_response_need"
  ],
  "geography_hints": [
    "United States"
  ],
  "confidence": "medium"
}
```

## Formation Rules

Form an `energy_flow_pressure_cluster` when all are true:

1. `2+` compatible `energy_flow_pressure_signal`s exist
2. the shared system is an actual energy or power-delivery system
3. the signals imply recurring pressure, not a single isolated mention
4. the cluster is tied to a concrete demand or buildout story

## What It Is For

This object should answer:

- do we have recurring physical-input pressure in an energy system?

It should not answer:

- whether direct capital deployment is already well evidenced
- whether the cluster alone justifies final narrowing
- whether a bottleneck layer is already known

## Failure Modes

1. `Macro electricity talk without system grounding`
2. `Generic industrial growth misread as energy pressure`
3. `Forecast-only cluster with no concrete demand/buildout context`

## Workflow Position

1. broad public flow
2. `energy_flow_pressure_signal`
3. `energy_flow_pressure_cluster`
4. merge review with capital-flow clusters
5. `structural_pressure_candidate`
