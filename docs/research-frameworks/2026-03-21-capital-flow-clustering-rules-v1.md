# Capital Flow Clustering Rules v1

Date: March 21, 2026

## Purpose

Define how `capital_flow_signal_candidate`s should be grouped into
`capital_flow_cluster`s.

This is a clustering contract, not a ranking model.

## Facts

1. `capital_flow_signal_candidate`s are artifact-local.
2. Artifact-local signals are too granular to justify pressure formation on
   their own.
3. Capital-flow clustering should privilege:
   - recurring spend/buildout evidence
   - system compatibility
   - time compatibility
4. Capital-flow clustering should not require energy-pressure evidence.

## Assumptions

1. v1 should prefer under-merging to over-merging.
2. Capital-flow clusters should be explainable with simple deterministic rules.
3. We should not optimize for maximum recall before we have more audited corpus
   runs.

## Definition

Two `capital_flow_signal_candidate`s are cluster-compatible when they are
compatible on:

1. system
2. direction
3. time

And they are not clearly incompatible on:

1. geography
2. demand story
3. buildout lane

## Required Inputs

Every candidate considered for clustering should expose:

1. `artifact_id`
2. `source_class`
3. `published_at`
4. `implied_capital_flow_mechanism`
5. `affected_system_hints`
6. `geography_hints`
7. `directness`
8. `confidence`

## Clustering Dimensions

### 1. System compatibility

Signals are compatible if they point to:

1. the same system label
2. adjacent system labels inside one buildout lane

Examples:

- `utility grid equipment` + `transformer production`
- `data center campus buildout` + `hyperscale power infrastructure`

Not compatible:

- `grid transformers` + `biopharma manufacturing`

### 2. Direction compatibility

Signals must imply the same directional story:

1. rising spend
2. expanding capacity
3. committed buildout
4. financing/procurement supporting expansion

Do not cluster:

- expansion signals with obvious contraction signals

### 3. Time compatibility

Signals should fall within:

1. the same rolling window
2. or adjacent time buckets

Recommended v1 default:

- `90` day rolling window

### 4. Geography compatibility

Signals are stronger when geography overlaps:

1. same country
2. same region
3. same corridor

Geography mismatch does not always block clustering, but it lowers confidence.

### 5. Demand-story compatibility

Signals should share a plausible common driver:

1. data-center load growth
2. grid modernization
3. AI campus buildout
4. transformer shortage response

## Hard Exclusions

Do not cluster together when any are true:

1. system labels are clearly unrelated
2. one signal is about buildout and the other is about maintenance-only activity
3. published dates are too far apart for the same rolling window
4. one signal materially contradicts the direction of the other

## Minimum Formation Rule

Form a `capital_flow_cluster` when all are true:

1. `2+` compatible `capital_flow_signal_candidate`s exist
2. at least `2` independent artifacts support the cluster
3. a concrete `system_label` can be named
4. a coherent `cluster_statement` can be written in one sentence

## Confidence Guidance

### `low`

- only the minimum signal count
- weak source diversity
- weak geography overlap

### `medium`

- `3+` compatible signals
- at least `2` source artifacts
- concrete system label
- coherent demand driver

### `high`

- repeated compatible signals across source classes
- persistent through time
- strong geography and system overlap
- clear capital-flow mechanism recurrence

For `trade_press`-only clusters, repeated coverage from one publication should
count less than cross-publication reinforcement.

That means `high` confidence should require at least one of:

1. `2+` source classes
2. `2+` distinct trade-press publishers with repeated compatible coverage

## Output Requirements

Every `capital_flow_cluster` should include:

1. `capital_flow_cluster_id`
2. `as_of_date`
3. `system_label`
4. `cluster_statement`
5. `supporting_capital_flow_signal_ids`
6. `signal_count`
7. `source_classes`
8. `time_window`
9. `geography_hints`
10. `demand_driver_summary`
11. `confidence`
12. `publisher_or_authors`
13. `publisher_diversity_count`
14. `publisher_diversity_status`

## Non-Goals

This step is not trying to:

1. identify the best public company expression
2. prove an upstream bottleneck
3. merge with energy-flow pressure yet
4. optimize numerical scoring

## Open Questions

1. Should same-publisher trade-press repetition lower `medium` confidence too,
   not just block `high`?
2. Should publisher diversity be weighted separately from source-class
   diversity in final cluster scoring?
