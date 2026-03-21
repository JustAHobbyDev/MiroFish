# Mixed Structural Pressure Candidates v2 Assessment

Date: March 21, 2026

## Scope

Assess the mixed-source rerun after:

1. adding a larger `company_release` batch
2. adding the boundedness gate

Primary artifact:

- `research/archive/normalized/mixed_source/mixed_structural_pressure_candidates_v2.json`

## Facts

1. Structural-pressure candidates: `8`
2. Corroborated candidates: `2`
3. Corroborated and bounded:
   - `1`
4. Corroborated but still too broad:
   - `1`
5. Uncorroborated but still promising upstream objects:
   - `6`

## Category Split

### Corroborated and Bounded

1. `spc_grid_equipment_and_transformer_buildout_2025-11-19_b00c1eaa`

Why it matters:

1. `company_release` and `trade_press` reinforce the same transformer and grid-equipment lane
2. the system label is concrete enough to bound a review universe
3. `bounded_universe_promotion_ready = true`

### Corroborated but Too Broad

1. `spc_industrial_manufacturing_expansion_2026-01-09_a5b69960`

Why it is still blocked:

1. source diversity corroboration is real
2. but the system label remains too broad
3. `bounded_universe_promotion_ready = false`

This is the key proof that corroboration is necessary but not sufficient.

### Uncorroborated but Promising Upstream Objects

1. `spc_data_center_power_demand_buildout_2025-10-30_d803ed8b`
2. `spc_grid_equipment_and_transformer_pressure_2025-03-10_0f431d4d`
3. `spc_power_generation_and_backup_equipment_pressure_2025-07-16_2de20001`
4. `spc_utility_and_large_load_power_demand_pressure_2025-04-07_94308007`
5. `spc_utility_and_large_load_power_demand_pressure_2025-10-30_c23ed0b5`
6. `spc_industrial_manufacturing_expansion_2025-05-15_f8f01357`

Interpretation:

1. these remain useful upstream pressure objects
2. they should guide corroboration and deeper collection
3. they should not auto-drive bounded-universe formation yet

## Conclusion

The current gating logic now behaves coherently.

What is now true:

1. single-source pressure objects can exist
2. source diversity can upgrade them
3. boundedness can still block broad multi-source objects

This is the first point where the workflow distinguishes:

1. interesting pressure
2. corroborated pressure
3. promotion-ready pressure

## Recommendation

1. Keep the current corroboration rule
2. Keep the boundedness gate
3. Focus the next mixed-source expansion on:
   - data-center power
   - utility and large-load power
   - generation / backup equipment
so more lanes can actually test promotion readiness
