# Structural Pressure Merge Rules v1

Date: March 21, 2026

## Purpose

Define how upstream pressure clusters become a
`structural_pressure_candidate`.

This spec governs merge logic between:

1. `capital_flow_cluster`
2. `energy_flow_pressure_cluster`

## Facts

1. `capital_flow_cluster` and `energy_flow_pressure_cluster` represent different
   evidence lanes.
2. They should stay separate until each lane has internal coherence.
3. The strongest structural-pressure objects are formed when:
   - financial response
   - and physical input pressure
   reinforce the same system story

## Assumptions

1. Capital flow remains the primary lane in v1.
2. Energy flow is reinforcing unless it also contains strong
   infrastructure-response evidence.
3. v1 merge logic should be auditable, not model-magic.

## Merge Cases

### Case 1: Dual-lane merge

Merge a `capital_flow_cluster` and an `energy_flow_pressure_cluster` into one
`structural_pressure_candidate` when all are true:

1. `System overlap`
   - same or adjacent concrete system labels
2. `Time overlap`
   - compatible rolling windows
3. `Direction compatibility`
   - both point to rising demand / response need
4. `Demand-story compatibility`
   - both fit the same underlying buildout or load narrative

### Case 2: Capital-flow-only formation

A `capital_flow_cluster` may form a `structural_pressure_candidate` alone when
all are true:

1. system grounding is clear
2. stress rationale is explicit
3. the cluster already implies a plausible upstream bottleneck or capacity
   stress zone

### Case 3: Energy-flow-only hold

An `energy_flow_pressure_cluster` alone should usually remain upstream.

It may form a `structural_pressure_candidate` alone only when:

1. infrastructure-response need is explicit
2. the physical system is concrete
3. the pressure has repeated support
4. the resulting structural-pressure statement is specific enough to justify
   bounded-universe formation

## Hard Merge Exclusions

Do not merge when any are true:

1. system labels are unrelated
2. time windows materially diverge
3. one cluster implies response while the other implies no real stress
4. the merged statement becomes broader or vaguer than the inputs

## Merge Output Requirements

A merged `structural_pressure_candidate` should record:

1. `supporting_capital_flow_cluster_ids`
2. `supporting_energy_flow_pressure_cluster_ids`
3. `merge_basis`
4. `merged_system_label`
5. `pressure_statement`
6. `stress_rationale`
7. `confidence`
8. `source_diversity_status`
9. `requires_source_diversity_corroboration`

## Merge Basis Contract

`merge_basis` should explicitly state:

1. `system_overlap`
2. `time_overlap`
3. `direction_compatibility`
4. `demand_story_overlap`

Example:

```json
{
  "system_overlap": true,
  "time_overlap": true,
  "direction_compatibility": true,
  "demand_story_overlap": "data-center load growth is driving both utility response and transformer/equipment spend"
}
```

## Confidence Guidance

### `low`

- only one weak lane exists
- merge basis is narrow

### `medium`

- one strong lane or two compatible lanes
- system grounding is clear
- stress rationale is specific

### `high`

- both lanes reinforce the same concrete system
- time overlap is strong
- pressure statement is clear and bounded

## Source-Diversity Guardrail

1. A `structural_pressure_candidate` may still form from one source class.
2. If all supporting clusters come from only one source class:
   - confidence must not exceed `medium`
   - `source_diversity_status` should be `single_source_class`
   - `requires_source_diversity_corroboration` should be `true`
3. Single-source structural-pressure candidates are valid upstream objects, but
   they should not auto-drive bounded-universe formation without:
   - corroboration from another source class
   - or explicit analyst confirmation
4. Multi-source candidates may retain `high` confidence when the rest of the
   merge basis is strong.

## Decision Rule

For v1:

1. prefer `capital_flow_cluster + energy_flow_pressure_cluster`
2. allow `capital_flow_cluster` alone
3. be conservative with `energy_flow_pressure_cluster` alone

## Open Questions

1. Should a dual-lane merge require geography overlap explicitly in v1?
2. Should single-source corroboration be satisfied by:
   - one additional source class anywhere in the candidate
   - or one additional source class inside each supporting lane?
