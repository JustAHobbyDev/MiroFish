# Historical Signal Calibration Case Template v1

Date: March 20, 2026

## Purpose

Provide a reusable template for filling one historical calibration case under:

- [2026-03-20-historical-signal-calibration-framework-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-historical-signal-calibration-framework-v1.md)

Each case must include:

1. case definition
2. blind pass
3. oracle pass
4. metric table
5. calibration judgment

## Case Definition

### Case Name

- `...`

### Case Type

- `upstream_bottleneck_discovery`
- `cycle_expression_selection`
- `capacity_constrained_buildout`
- `control_case`

### Final Expression Or Bottleneck

- `...`

### Pre-Move Cutoff Date

- `...`

### Post-Cutoff Outcome Window

- `...`

### Allowed Public Source Universe

- `...`

### Time Bucket Rule

- `weekly` by default unless there is a strong reason to use another bucket

## Facts

1. `...`
2. `...`

## Assumptions

1. `...`
2. `...`

## Blind Pass

### Objective

- determine whether the system would have surfaced enough signal to justify narrowing without already knowing the answer

### Blind Rules Used

1. `...`
2. `...`

### Allowed Clustering Inputs

1. `...`
2. `...`

### Surfaced Signals

List the surfaced blind-pass signals as short bullets.

1. `...`
2. `...`

### Blind Role Coverage

- `demand_pressure`
- `system_grounding`
- `visible_beneficiary`
- `stress_hint`
- `upstream_clue`
- `bottleneck_verification`

Mark which were actually surfaced.

### Blind Judgment

- `blind_fail`
- `blind_partial`
- `blind_pass`

### Why

1. `...`
2. `...`

## Oracle Pass

### Objective

- determine how much relevant pre-move public signal actually existed

### Oracle Rules Used

1. `...`
2. `...`

### Oracle Relevant Signals

List the oracle-labeled relevant signals as short bullets.

1. `...`
2. `...`

### Oracle Role Coverage

- `demand_pressure`
- `system_grounding`
- `visible_beneficiary`
- `stress_hint`
- `upstream_clue`
- `bottleneck_verification`

Mark which were actually present.

### Earliest Oracle Narrowing Date

- `...`

## Metrics

### Blind Metrics

- `blind_surfaced_signal_count`:
- `blind_independent_signal_count`:
- `blind_source_count`:
- `blind_source_class_count`:
- `blind_time_bucket_count`:
- `blind_role_coverage`:
- `blind_structural_pressure_candidate_formed`:
- `blind_narrowing_justified`:

### Oracle Metrics

- `oracle_observed_signal_count`:
- `oracle_independent_signal_count`:
- `oracle_source_count`:
- `oracle_source_class_count`:
- `oracle_time_bucket_count`:
- `oracle_role_coverage`:
- `oracle_earliest_narrowing_date`:

### Derived Comparison Metrics

- `blind_recall_ratio`:
- `blind_role_coverage_ratio`:
- `narrowing_gap_days`:

## Calibration Judgment

### What This Case Says

1. `...`
2. `...`

### Threshold Implication

1. `...`
2. `...`

### Caveats

1. `...`
2. `...`

## Open Questions

1. `...`
2. `...`
