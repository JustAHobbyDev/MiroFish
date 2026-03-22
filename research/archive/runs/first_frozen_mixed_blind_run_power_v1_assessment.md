# First Frozen Mixed Blind Run Power Assessment v1

Date: March 22, 2026

## Purpose

Evaluate the first executed frozen mixed-corpus blind run after outputs were
frozen.

This is the first honest answer to:

1. Can the system form the right universes from a mixed corpus without
   benchmark-seeded clustering?
2. Is universe discovery strong enough to matter even if final expression
   discovery remains weaker?

## Facts

### Corpus and freeze

1. Executed corpus window:
   - `2025-09-01` to `2026-02-28`
2. Source classes used:
   - `company_release`
   - `government`
   - `trade_press`
3. This is a partial-coverage run against the broader draft blind-run manifest.
4. A date-window freezer was applied before the authoritative freeze because
   the naive first pass leaked older trade-press artifacts.
5. The authoritative outputs are the `v2` window-filtered mixed artifacts.

### Frozen output counts

1. Mixed prefilter processed artifacts:
   - `324`
2. Mixed prefilter kept artifacts:
   - `41`
3. Mixed prefilter review artifacts:
   - `5`
4. Mixed capital-signal artifacts sent to LLM:
   - `46`
5. Mixed capital-signal successful extractions:
   - `43`
6. Mixed capital-signal total candidates:
   - `53`
7. Capital-flow clusters:
   - `6`
8. Energy-flow clusters:
   - `1`
9. Structural-pressure candidates:
   - `7`
10. `enough_to_narrow`:
    - `3`
11. `not_enough_to_narrow`:
    - `4`

### Promotion-ready bounded universes

1. `data center campus buildout`
2. `grid equipment and transformer buildout`
3. `utility and large-load power buildout`

### Blocked or held lanes

1. `general industrial buildout`
   - blocked as too broad
2. `industrial manufacturing expansion`
   - blocked as too broad
3. `power generation and backup equipment buildout`
   - blocked as too broad
4. `utility and large-load power demand pressure`
   - blocked as bounded but uncorroborated single-source trade press

## Assessment

### Universe discovery

Result:
- `blind_pass`

Why:
1. The run surfaced three coherent bounded universes from mixed-source inputs.
2. The run did not just promote every corroborated lane.
3. The strongest surfaced lane was:
   - `grid equipment and transformer buildout`
4. The run also recovered:
   - `data center campus buildout`
   - `utility and large-load power buildout`

This is strong enough to count as real universe discovery for a first frozen
partial run.

### Final expression discovery

Result:
- `not_proven`

Why:
1. The blind-run protocol freezes at structural-pressure and narrowing outputs,
   not final public-expression ranking.
2. The in-window trade-press set was sparse, so the power branch stayed broader
   than the later manually expanded downstream pipeline.
3. This run proves:
   - pressure-universe formation
4. It does not yet prove:
   - best-expression recovery

### What this run actually demonstrates

The run demonstrates that the system can:

1. take mixed-source inputs
2. form structural-pressure candidates
3. justify narrowing into bounded universes
4. reject broader or weaker lanes

without using benchmark-seeded renaming or post-freeze source additions.

That is meaningful.

It is not yet proof that the system can recover the final best ticker or
expression early enough.

## Decision

Current posture:

1. universe discovery:
   - stronger than before
2. final expression discovery:
   - still unproven

This is exactly the kind of result that should increase confidence in the
architecture while still withholding claims about full AleaBito-style
expression recovery.

## Next Implication

The next honest proof step is not new source collection.

It is:

1. freeze entity-surfacing as part of the blind-run output set
2. run the same blind procedure on another historical mixed corpus
3. compare:
   - bounded-universe recovery
   - candidate-expression surfacing
   - final-expression recovery

## References

- [first_frozen_mixed_blind_run_power_prefilter_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_prefilter_v2.json)
- [first_frozen_mixed_blind_run_power_capital_signal_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_capital_signal_v2.json)
- [first_frozen_mixed_blind_run_power_capital_flow_clusters_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_capital_flow_clusters_v2.json)
- [first_frozen_mixed_blind_run_power_energy_flow_clusters_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_energy_flow_clusters_v2.json)
- [first_frozen_mixed_blind_run_power_structural_pressure_candidates_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_structural_pressure_candidates_v2.json)
- [first_frozen_mixed_blind_run_power_bounded_universe_candidates_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_bounded_universe_candidates_v2.json)
- [first_frozen_mixed_blind_run_power_v1_run_log.json](/Users/danielschmidt/dev/MiroFish/research/archive/runs/first_frozen_mixed_blind_run_power_v1_run_log.json)
- [first_frozen_mixed_blind_run_power_v1_narrowing_decisions.json](/Users/danielschmidt/dev/MiroFish/research/archive/runs/first_frozen_mixed_blind_run_power_v1_narrowing_decisions.json)
