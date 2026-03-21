# Mixed Structural Pressure Candidates v3 Assessment

Date: March 21, 2026

## Scope

Assess the mixed-source rerun after:

1. publisher-diversity weighting in clustering
2. bounded-universe formation support

Primary artifacts:

1. `research/archive/normalized/mixed_source/mixed_structural_pressure_candidates_v3.json`
2. `research/archive/normalized/mixed_source/mixed_bounded_universe_candidates_v1.json`

## Facts

1. Structural-pressure candidates: `8`
2. Corroborated candidates: `2`
3. Promotion-ready structural-pressure candidates: `1`
4. Bounded-universe candidates formed: `1`

## What Changed

### Publisher-diversity weighting

The new weighting reduced confidence inflation from repeated single-publication
coverage.

Examples:

1. `power generation and backup equipment buildout`
   - stays `medium`
   - `publisher_diversity_status = single_publisher`

2. `data center campus buildout`
   - can still reach `high`
   - `publisher_diversity_status = multi_publisher`

3. `grid equipment and transformer buildout`
   - corroborated mixed-source lane remains `high`

### Bounded-universe formation

Only one candidate now passes all gates:

1. `grid equipment and transformer buildout`

It becomes:

1. `buc_grid_equipment_and_transformer_buildout_2025-11-19_b00c1eaa`

## Interpretation

The pipeline now distinguishes four levels cleanly:

1. upstream pressure
2. corroborated pressure
3. corroborated and bounded pressure
4. bounded-universe candidate

That is the first end-to-end shape that does not jump directly from public
signals into ticker hunting.

## Conclusion

The current result is coherent:

1. mixed-source transformer/grid-equipment pressure is ready for bounded-universe work
2. corroborated industrial manufacturing pressure is still too broad
3. uncorroborated power and utility lanes remain upstream

## Recommendation

1. Use the transformer bounded-universe candidate as the first downstream test case
2. Expand corroboration coverage next for:
   - utility and large-load power
   - data-center power
   - power generation / backup equipment
