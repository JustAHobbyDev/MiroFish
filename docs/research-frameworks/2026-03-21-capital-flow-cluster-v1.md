# Capital Flow Cluster v1

Date: March 21, 2026

## Purpose

Define the first aggregation object above `capital_flow_signal_candidate`.

This object exists to group multiple artifact-local capital-flow signals into a
 coherent provisional pattern before any merge with other pressure lanes.

It is:

- upstream of `structural_pressure_candidate`
- downstream of `capital_flow_signal_candidate`
- narrower than broad theme detection

## Facts

1. A single capital-flow signal is too weak to justify structural-pressure
   formation.
2. Multiple capital-flow signals can still be noisy if they are not grouped by:
   - shared system hints
   - shared demand story
   - shared geography or buildout corridor
3. `capital_flow_signal_candidate` and `energy_flow_pressure_signal` should not
   be merged immediately because they represent different evidence types.

## Definition

A `capital_flow_cluster` is a bounded grouping of compatible
`capital_flow_signal_candidate`s that suggests directional spend, buildout,
procurement, or financing is recurring within the same provisional system.

## Required Invariants

Every valid `capital_flow_cluster` must have:

1. `Signal plurality`
   - at least two supporting `capital_flow_signal_candidate`s
2. `Compatibility`
   - signals do not conflict on direction or system
3. `Shared provisional system`
   - the cluster can name a concrete system, buildout lane, or industrial layer
4. `Explicit time boundary`
   - supporting evidence lives within a defined window
5. `Source provenance`
   - every member signal is traceable

## Minimal Shape

```json
{
  "capital_flow_cluster_id": "cfc_grid_buildout_2026_02_28_v1",
  "as_of_date": "2026-02-28",
  "status": "candidate",
  "system_label": "US grid equipment and utility buildout",
  "cluster_statement": "Multiple public artifacts imply rising spend and buildout around grid equipment, transmission, and utility response to large-load demand.",
  "supporting_capital_flow_signal_ids": [
    "cfs_101",
    "cfs_118",
    "cfs_142"
  ],
  "signal_count": 3,
  "source_classes": [
    "trade_press",
    "company_release"
  ],
  "time_window": {
    "start_date": "2025-12-01",
    "end_date": "2026-02-28"
  },
  "geography_hints": [
    "United States"
  ],
  "demand_driver_summary": "Large-load, data-center, and utility expansion needs are driving equipment and infrastructure spend.",
  "confidence": "medium"
}
```

## Formation Rules

Form a `capital_flow_cluster` when all are true:

1. `2+` compatible `capital_flow_signal_candidate`s exist
2. at least `2` independent artifacts support the cluster
3. the system label is concrete
4. the cluster statement is about recurring spend, buildout, procurement, or
   financing

## What It Is For

This object should answer:

- do we have recurring financial-response evidence in one provisional system?

It should not answer:

- whether energy or other production-input pressure also exists
- whether the final bottleneck layer is known
- whether a bounded universe should already be formed

## Failure Modes

1. `Narrative-only cluster`
   - the cluster groups theme talk without concrete spend/buildout evidence
2. `Issuer echo cluster`
   - multiple signals reduce to one company repeating itself
3. `System blur`
   - the cluster is too broad to name a real industrial lane

## Workflow Position

1. broad public flow
2. `capital_flow_signal_candidate`
3. `capital_flow_cluster`
4. merge review with other pressure clusters
5. `structural_pressure_candidate`
