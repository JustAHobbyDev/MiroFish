# First Frozen Mixed Blind Run Power Assessment v1

Date: March 22, 2026

## Purpose

Re-evaluate the first executed frozen mixed-corpus blind run after removing
synthetic archive inputs from evaluation.

## Facts

### Corpus and freeze

1. Executed corpus window:
   - `2025-09-01` to `2026-02-28`
2. Source classes used in the rebuilt baseline:
   - `government`
   - `trade_press`
3. This is a partial-coverage real-only baseline.
4. The earlier synthetic company-release archive slice was removed from evaluation.
5. The authoritative outputs are the rebuilt `v2`/`v1` files listed below.

### Frozen output counts

1. Mixed prefilter processed artifacts:
   - `306`
2. Mixed prefilter kept artifacts:
   - `29`
3. Mixed prefilter review artifacts:
   - `4`
4. Mixed capital-signal artifacts sent to LLM:
   - `33`
5. Mixed capital-signal successful extractions:
   - `30`
6. Mixed capital-signal total candidates:
   - `24`
7. Capital-flow clusters:
   - `2`
8. Energy-flow clusters:
   - `1`
9. Structural-pressure candidates:
   - `3`
10. `enough_to_narrow`:
    - `0`
11. `not_enough_to_narrow`:
    - `3`

### Remaining structural candidates

1. `industrial manufacturing expansion`
   - blocked as too broad
2. `power generation and backup equipment buildout`
   - blocked as too broad
3. `utility and large-load power demand pressure`
   - bounded but uncorroborated

## Assessment

### Universe discovery

Result:
- `not_proven_after_cleanup`

Why:
1. The cleaned real-only run surfaces zero promotion-ready bounded universes.
2. The remaining lanes do not clear the bounded-universe gate.
3. That means the earlier `blind_pass` conclusion cannot stand as the authoritative baseline.

### Final expression discovery

Result:
- `not_proven`

Why:
1. The cleaned run does not reach promotion-ready universes.
2. Entity surfacing therefore stops at zero on the authoritative evaluation path.
3. So there is no basis for a final-expression claim in this window.

## Decision

Current posture:

1. the cleaned real-only baseline is weaker than the prior mixed-through-synthetic interpretation
2. this corpus/window no longer proves blind universe discovery
3. the architecture still may be directionally right, but this run is no longer evidence of success

## Implication

The next honest proof step is:

1. build another true blind-ready corpus with enough real-only source coverage
2. or re-scope the window so real corroborating evidence actually exists inside the freeze
3. then rerun the full blind path on that stronger baseline

## References

- [first_frozen_mixed_blind_run_power_prefilter_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_prefilter_v2.json)
- [first_frozen_mixed_blind_run_power_capital_signal_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_capital_signal_v2.json)
- [first_frozen_mixed_blind_run_power_capital_flow_clusters_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_capital_flow_clusters_v2.json)
- [first_frozen_mixed_blind_run_power_energy_flow_clusters_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_energy_flow_clusters_v2.json)
- [first_frozen_mixed_blind_run_power_structural_pressure_candidates_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_structural_pressure_candidates_v2.json)
- [first_frozen_mixed_blind_run_power_bounded_universe_candidates_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_bounded_universe_candidates_v2.json)
- [first_frozen_mixed_blind_run_power_entity_freeze_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_entity_freeze_v1.json)
- [first_frozen_mixed_blind_run_power_v1_run_log.json](/Users/danielschmidt/dev/MiroFish/research/archive/runs/first_frozen_mixed_blind_run_power_v1_run_log.json)
- [first_frozen_mixed_blind_run_power_v1_narrowing_decisions.json](/Users/danielschmidt/dev/MiroFish/research/archive/runs/first_frozen_mixed_blind_run_power_v1_narrowing_decisions.json)
