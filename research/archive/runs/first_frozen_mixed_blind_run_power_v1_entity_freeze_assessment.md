# First Frozen Mixed Blind Run Power Entity Freeze Assessment v1

Date: March 22, 2026

## Purpose

Extend the first frozen mixed blind run through deterministic entity surfacing
so the project can judge whether the run is getting closer to final-expression
recovery.

## Facts

### Frozen entity-surfacing output

- [first_frozen_mixed_blind_run_power_entity_freeze_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_entity_freeze_v1.json)

### Counts

1. Input bounded universes:
   - `3`
2. Bounded research sets:
   - `3`
3. Bounded entity candidates:
   - `25`
4. `real_only` entity candidates:
   - `8`
5. `synthetic_only` entity candidates:
   - `17`

### By universe

1. `data center campus buildout`
   - matched artifacts: `12`
   - entity candidates: `11`
   - real-only entities:
     - `DTE`
     - `FirstEnergy`
     - `Southern`
     - `Rockwell Automation`

2. `grid equipment and transformer buildout`
   - matched artifacts: `6`
   - entity candidates: `6`
   - real-only entities:
     - `Hitachi`

3. `utility and large-load power buildout`
   - matched artifacts: `9`
   - entity candidates: `8`
   - real-only entities:
     - `DTE`
     - `Southern`
     - `FirstEnergy`

## Assessment

### What improved

1. The blind-run output set now includes deterministic entity surfacing.
2. The run no longer stops at universe formation alone.
3. Real entities do appear inside all three promotion-ready universes.

### What did not improve enough

1. Synthetic-only names still dominate the raw surfaced set.
2. The transformer lane, which matters most for bottleneck-style final picks,
   surfaced only one real supplier name:
   - `Hitachi`
3. The later downstream public-market names:
   - `GE Vernova`
   - `Eaton`
   do not emerge from this frozen corpus alone.

## Judgment

Result:
- `partial_pass`

Meaning:
1. entity surfacing is now real and frozen
2. final-expression recovery is still not proven

This does strengthen the overall system claim a little:

1. universe discovery is not the only thing working
2. some candidate-expression surfacing exists

But it does **not** yet change the top-line conclusion:

- the system is still better at bounded-universe formation than final best
  expression discovery

## Implication

The next proof step should require:

1. a second true mixed-corpus blind run
2. with entity freeze included from the start
3. and with enough real-source coverage that synthetic-only names do not
   dominate the surfaced set
