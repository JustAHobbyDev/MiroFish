# Trade Press Structural Pressure Candidate Audit v1

Date: March 21, 2026

## Scope

Audit the guarded structural-pressure output:

- `research/archive/normalized/trade_press/trade_press_structural_pressure_candidates_v3.json`

## Facts

1. Candidate count: `6`
2. All `6` candidates are supported by only one source class:
   - `trade_press`
3. All `6` candidates now carry:
   - `source_diversity_status = single_source_class`
   - `requires_source_diversity_corroboration = true`
4. The new guardrail caps single-source candidates at `medium` confidence.

## Item Audit

### 1. `spc_data_center_power_demand_buildout_2025-10-30_d803ed8b`

- Label: `correct_candidate`
- Judgment:
  - recurrent data-center buildout
  - dual-lane reinforcement from capital-flow and energy-flow clusters
  - concrete system label
- Promotion note:
  - valid structural-pressure object
  - not ready for bounded-universe promotion without corroboration beyond `trade_press`

### 2. `spc_grid_equipment_and_transformer_pressure_2025-03-10_0f431d4d`

- Label: `correct_candidate`
- Judgment:
  - concrete transformer / grid-equipment system
  - repeated spend and pressure signals
  - clear stress rationale
- Promotion note:
  - valid structural-pressure object
  - should still require corroboration before bounded-universe promotion

### 3. `spc_industrial_manufacturing_expansion_2025-05-15_f8f01357`

- Label: `borderline_should_review`
- Judgment:
  - repeated industrial expansion exists
  - system label is too broad and generic relative to the other candidates
  - stress zone is not yet bounded tightly enough
- Promotion note:
  - useful upstream object
  - should not promote further without corroboration and narrower system definition

### 4. `spc_power_generation_and_backup_equipment_pressure_2025-07-16_2de20001`

- Label: `borderline_should_review`
- Judgment:
  - recurring generation / backup-power response is real
  - still broader and less clearly bottleneck-shaped than transformer or data-center power cases
- Promotion note:
  - acceptable structural-pressure object
  - should remain corroboration-gated before bounded-universe formation

### 5. `spc_utility_and_large_load_power_demand_pressure_2025-04-07_94308007`

- Label: `correct_candidate`
- Judgment:
  - repeated utility load-growth and infrastructure-response evidence
  - concrete power-demand stress system
  - enough coherence for a structural-pressure object
- Promotion note:
  - valid candidate
  - still single-source and should remain corroboration-gated

### 6. `spc_utility_and_large_load_power_demand_pressure_2025-10-30_c23ed0b5`

- Label: `correct_candidate`
- Judgment:
  - same system family as the earlier utility / large-load cluster
  - repeated late-window pressure evidence remains coherent
- Promotion note:
  - valid candidate
  - still single-source and should remain corroboration-gated

## Summary

1. `correct_candidate`: `4`
2. `borderline_should_review`: `2`
3. `false_positive`: `0`

## Recommendation

1. Keep source-diversity weighting at the `structural_pressure_candidate` layer.
2. Allow single-source structural-pressure candidates to exist.
3. Do not allow them to auto-drive bounded-universe formation.
4. Require:
   - corroboration from another source class
   - or explicit analyst promotion
before downstream narrowing.

## Conclusion

The `v3` guardrail is the right cut.

It preserves real upstream pressure objects while preventing a single-source
trade-press lane from overclaiming bounded-universe readiness.
