# Mixed Structural Pressure Candidates v1 Audit

Date: March 21, 2026

## Scope

Audit the first mixed-source structural-pressure output:

- `research/archive/normalized/mixed_source/mixed_structural_pressure_candidates_v1.json`

Inputs:

1. mixed capital clusters from:
   - `trade_press`
   - `company_release`
2. energy clusters from:
   - `trade_press`

## Facts

1. Candidate count: `8`
2. Single-source candidates: `6`
3. Corroborated multi-source candidates: `2`
4. Corroboration rule used:
   - `2+` distinct source classes across supporting clusters
   - and at least `1` supporting `capital_flow_cluster`

## Item Audit

### 1. `spc_data_center_power_demand_buildout_2025-10-30_d803ed8b`

- Label: `correct_candidate`
- Source diversity: `single_source_class`
- Corroboration satisfied: `false`
- Judgment:
  - coherent dual-lane trade-press candidate
  - still requires corroboration

### 2. `spc_grid_equipment_and_transformer_pressure_2025-03-10_0f431d4d`

- Label: `correct_candidate`
- Source diversity: `single_source_class`
- Corroboration satisfied: `false`
- Judgment:
  - coherent dual-lane trade-press candidate
  - still requires corroboration

### 3. `spc_grid_equipment_and_transformer_buildout_2025-09-18_24176b1d`

- Label: `correct_candidate`
- Source diversity: `multi_source_class`
- Corroboration satisfied: `true`
- Judgment:
  - this is the clearest successful corroborated candidate
  - `company_release` and `trade_press` reinforce the same transformer buildout lane
  - bounded-universe formation now looks justified

### 4. `spc_industrial_manufacturing_expansion_2025-05-15_f8f01357`

- Label: `borderline_should_review`
- Source diversity: `single_source_class`
- Corroboration satisfied: `false`
- Judgment:
  - too broad and generic
  - valid upstream object, not ready for narrowing

### 5. `spc_industrial_manufacturing_expansion_2026-01-09_a5b69960`

- Label: `borderline_should_review`
- Source diversity: `multi_source_class`
- Corroboration satisfied: `true`
- Judgment:
  - corroboration is real
  - but the system label remains too broad
  - this proves source diversity is necessary but not sufficient

### 6. `spc_power_generation_and_backup_equipment_pressure_2025-07-16_2de20001`

- Label: `borderline_should_review`
- Source diversity: `single_source_class`
- Corroboration satisfied: `false`
- Judgment:
  - plausible structural pressure
  - still too broad for downstream promotion without corroboration

### 7. `spc_utility_and_large_load_power_demand_pressure_2025-04-07_94308007`

- Label: `correct_candidate`
- Source diversity: `single_source_class`
- Corroboration satisfied: `false`
- Judgment:
  - coherent upstream pressure object
  - energy-only and should remain promotion-gated

### 8. `spc_utility_and_large_load_power_demand_pressure_2025-10-30_c23ed0b5`

- Label: `correct_candidate`
- Source diversity: `single_source_class`
- Corroboration satisfied: `false`
- Judgment:
  - coherent upstream pressure object
  - energy-only and should remain promotion-gated

## Summary

1. `correct_candidate`: `5`
2. `borderline_should_review`: `3`
3. `false_positive`: `0`
4. `corroborated_and_narrow_enough`: `1`
5. `corroborated_but_still_too_broad`: `1`

## Conclusion

The corroboration rule is useful.

It does not create quality by itself.

What it does do:

1. distinguish single-source upstream objects from cross-source reinforced ones
2. correctly upgrade the transformer buildout lane
3. avoid over-promoting energy-only pressure objects

What it does not do:

1. rescue broad labels like `industrial manufacturing expansion`
2. replace the need for concrete system bounding

## Recommendation

1. Keep the corroboration rule as implemented.
2. Treat corroboration as:
   - necessary for auto-promotion
   - not sufficient for auto-promotion
3. Add a separate boundedness check before `structural_pressure_candidate -> bounded universe`.
