# First Frozen Mixed Blind Run Power Entity Freeze Assessment v1

Date: March 22, 2026

## Purpose

Re-evaluate the frozen entity surface after removing synthetic archive inputs from
blind-run evaluation.

## Facts

### Frozen entity-surfacing output

- [first_frozen_mixed_blind_run_power_entity_freeze_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/first_frozen_mixed_blind_run_power_entity_freeze_v1.json)

### Counts

1. Input bounded universes:
   - `3`
2. Bounded research sets:
   - `3`
3. Bounded entity candidates:
   - `8`
4. `real_only` entity candidates:
   - `8`
5. `synthetic_only` entity candidates:
   - `0`

### By universe

1. `data center campus buildout`
   - matched artifacts: `5`
   - entity candidates: `4`
   - real-only entities:
     - `DTE`
     - `FirstEnergy`
     - `Southern`
     - `Rockwell Automation`

2. `grid equipment and transformer buildout`
   - matched artifacts: `1`
   - entity candidates: `1`
   - real-only entities:
     - `Hitachi`

3. `utility and large-load power buildout`
   - matched artifacts: `4`
   - entity candidates: `3`
   - real-only entities:
     - `DTE`
     - `Southern`
     - `FirstEnergy`

## Assessment

### What improved

1. The blind-run entity surface is now measured on real-only evidence.
2. Synthetic archive names no longer dominate the surfaced set.
3. The resulting measurement is more defensible for final-expression evaluation.

### What still does not improve enough

1. The transformer lane still surfaces only one real supplier name:
   - `Hitachi`
2. The later downstream public-market names:
   - `GE Vernova`
   - `Eaton`
   do not emerge from this frozen corpus alone.
3. So the system is cleaner to evaluate now, but still weak on final-expression recovery.

## Judgment

Result:
- `partial_pass`

Meaning:
1. entity surfacing now survives a real-only cleanup
2. final-expression recovery is still not proven

## Implication

The next proof step should require:

1. real-only entity surfacing by default
2. a second true mixed-corpus blind run
3. enough real-source coverage that constrained-layer suppliers surface before downstream hindsight fills the gap
