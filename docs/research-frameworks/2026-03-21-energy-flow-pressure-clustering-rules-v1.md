# Energy Flow Pressure Clustering Rules v1

Date: March 21, 2026

## Purpose

Define how `energy_flow_pressure_signal`s should be grouped into
`energy_flow_pressure_cluster`s.

This step should preserve physically important pressure signals without
 weakening the direct capital-flow lane.

## Facts

1. Energy-flow signals can be valid even when direct capital-flow evidence is
   still weak.
2. Utility load-growth, interconnection, and infrastructure-response signals
   recur differently from spend/buildout signals.
3. Energy-flow clustering should focus on physical pressure coherence, not
   financial-response coherence.

## Assumptions

1. v1 should remain energy-specific, not general production-input clustering.
2. Utility/load articles can cluster together even when they stay review-stage
   in the capital-flow lane.
3. We should not merge generic industrial-energy inference into this lane.

## Definition

Two `energy_flow_pressure_signal`s are cluster-compatible when they are
compatible on:

1. energy system
2. pressure orientation
3. time

And they are not clearly incompatible on:

1. geography
2. demand story
3. pressure direction

## Required Inputs

Every candidate considered for clustering should expose:

1. `artifact_id`
2. `source_class`
3. `published_at`
4. `energy_pressure_type`
5. `relationship_to_capital_flow`
6. `system_hints`
7. `physical_implication`
8. `confidence`

## Clustering Dimensions

### 1. Energy-system compatibility

Signals are compatible if they point to:

1. the same power-delivery system
2. adjacent layers in the same energy-response chain

Examples:

- utility load growth + interconnection pipeline pressure
- transformer shortage + transformer-plant buildout
- new generation response + large-load demand surge

### 2. Pressure-type compatibility

Signals may cluster when pressure types are adjacent:

1. `load_growth`
2. `pipeline_pressure`
3. `capacity_tightness`
4. `infrastructure_response_need`

Preferred compatible combinations:

- `load_growth` + `pipeline_pressure`
- `pipeline_pressure` + `infrastructure_response_need`
- `capacity_tightness` + `infrastructure_response_need`

### 3. Time compatibility

Recommended v1 default:

- `90` day rolling window

Signals outside the same rolling window should not cluster in v1.

### 4. Geography compatibility

Energy systems are often geographic.

So geography should matter more here than in some capital-flow clusters.

Preferred:

1. same utility footprint
2. same state or corridor
3. same national grid context

### 5. Demand-story compatibility

Signals should share one of:

1. data-center load growth
2. hyperscale campus buildout
3. grid equipment stress
4. generation-response need

## Hard Exclusions

Do not cluster when any are true:

1. one signal is generic industrial energy inference with no explicit
   energy-system linkage
2. system hints are clearly unrelated
3. pressure directions conflict
4. the only overlap is broad macro electricity demand talk

## Minimum Formation Rule

Form an `energy_flow_pressure_cluster` when all are true:

1. `2+` compatible `energy_flow_pressure_signal`s exist
2. at least `2` independent artifacts support the cluster
3. the energy system can be named concretely
4. the cluster statement describes recurring physical pressure

## Confidence Guidance

### `low`

- minimum signal count
- weak geography coherence
- weak pressure-type reinforcement

### `medium`

- `3+` compatible signals
- concrete energy system
- recurring pressure type or adjacent pressure types

### `high`

- persistent signals through time
- strong geography overlap
- clear infrastructure-response implications

For `trade_press`-only clusters, repeated coverage from one publication should
count less than cross-publication reinforcement.

That means `high` confidence should require at least one of:

1. `2+` source classes
2. `2+` distinct trade-press publishers with repeated compatible coverage

## Output Requirements

Every `energy_flow_pressure_cluster` should include:

1. `energy_flow_pressure_cluster_id`
2. `as_of_date`
3. `system_label`
4. `cluster_statement`
5. `supporting_energy_flow_signal_ids`
6. `signal_count`
7. `source_classes`
8. `time_window`
9. `pressure_types_present`
10. `geography_hints`
11. `confidence`
12. `publisher_or_authors`
13. `publisher_diversity_count`
14. `publisher_diversity_status`

## Non-Goals

This step is not trying to:

1. prove capital allocation already exists
2. rank company expressions
3. infer non-energy production-input pressure
4. merge with capital-flow clusters yet

## Open Questions

1. Should utility-load forecasts without any explicit infrastructure-response
   language ever form a cluster on their own?
2. Should the v1 geography rule be stricter for utility articles than for
   transformer-equipment articles?
