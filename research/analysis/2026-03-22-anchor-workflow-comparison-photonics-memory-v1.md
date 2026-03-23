# Anchor Workflow Comparison: Photonics vs Memory v1

Date: March 22, 2026

Inputs:

- [2026-03-22-aleabitoreddit-photonics-anchor-workflow-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-22-aleabitoreddit-photonics-anchor-workflow-v1.json)
- [2026-03-22-aleabitoreddit-memory-anchor-workflow-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-22-aleabitoreddit-memory-anchor-workflow-v1.json)
- [third_historical_mixed_corpus_photonics_anchor_first_replay_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/third_historical_mixed_corpus_photonics_anchor_first_replay_v2.json)

## Facts

1. The photonics case starts from a visible single-company clue.
- `LITE`

2. The memory case starts from a visible cycle anchor and then an anchor set.
- `MU`
- `SK Hynix`
- `Samsung`

3. The photonics case reaches the upstream chokepoint by tracing dependencies from the anchor.
- `LITE -> COHR / AAOI -> AXTI`

4. The memory case reaches `SNDK` only after the cycle is already legible.
- `MU / SK Hynix / Samsung -> memory supercycle -> SNDK`

5. The rebuilt seeded photonics replay now supports the full named chain through `AXT`.
- but only inside a retrospective-seeded corpus

## Conclusion

The same sequence does **not** hold across both cases.

### Photonics workflow family

1. `anchor_clue_detection`
2. `system_demand_mapping`
3. `anchor_expression_confirmation`
4. `adjacent_expression_expansion`
5. `upstream_chokepoint_tracing`

### Memory workflow family

1. `cycle_clue_detection`
2. `anchor_set_formation`
3. `stress_confirmation`
4. `expression_selection`
5. `second_order_followon_mapping`

## Product Implication

MiroFish should support at least two workflow families:

1. `anchor_dependency_workflow`
- best fit:
  - photonics
  - component bottleneck lanes

2. `cycle_expression_workflow`
- best fit:
  - memory
  - pricing-power / supply-tightness cycles

## Practical Read

1. The earlier assumption that one blind recipe should fit both cases is wrong.
2. The next useful architecture step is not more downstream ranking.
3. It is lane-family routing:
- detect whether a case is:
  - anchor/dependency-driven
  - or cycle/expression-driven

## Assumptions

1. The archive order is close enough to research order to guide product design.
2. These two cases are representative enough to justify at least a two-family workflow split.

## Speculative

1. Additional families may emerge later:
- policy-shock workflow
- operator-capex workflow

## Open Questions

1. What heuristics should route a lane into:
- `anchor_dependency_workflow`
- vs `cycle_expression_workflow`?
2. Should `anchor_set` become a first-class object alongside `anchor_expression`?
