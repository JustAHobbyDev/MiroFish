# Frozen Blind Run Comparison v1

Date: March 22, 2026

## Purpose

Compare the first true mixed-corpus blind run against the existing curated
historical calibration cases after synthetic cleanup and full real-only rerun.

## Facts

### Case 1

`first_frozen_mixed_blind_run_power_v1`

1. type:
   - `true_mixed_corpus_blind_run`
2. universe discovery:
   - `not_proven_after_cleanup`
3. narrowing:
   - `0`
4. final expression:
   - `not_proven`
5. entity surfacing:
   - `no_real_only_downstream_surface`

### Case 2

`Photonics -> AXTI`

1. type:
   - `curated_historical_calibration`
2. universe discovery:
   - `blind_pass`
3. narrowing:
   - `1`
4. final expression:
   - `not_proven`
5. entity / upstream clue state:
   - upstream clue present

### Case 3

`Memory -> SNDK`

1. type:
   - `curated_historical_calibration`
2. universe discovery:
   - `blind_pass`
3. narrowing:
   - `1`
4. final expression:
   - `not_proven`
5. entity / expression state:
   - candidate expression visible but not strong

## Assessment

### What the cleaned mixed run now proves

1. The measurement is now honest and real-only.
2. Synthetic contamination is no longer inflating the apparent result.
3. That honesty matters more than preserving the earlier favorable interpretation.

### What it now shows

1. The cleaned mixed run no longer reaches promotion-ready bounded universes.
2. So it does not currently match the curated cases even on universe discovery.
3. The architecture may still be promising, but this run is not evidence of success.

## Second True Mixed Run Status

Status:
- `not executed`

Reason:
1. A second historical mixed corpus now exists.
2. But the current HBM and photonics corpora are retrospective-seeded.
3. They are useful for comparison and stress testing, not yet honest frozen blind runs.

## Judgment

Current best read:

1. the project still has promising curated calibrations
2. but the first real-only mixed blind baseline is not yet strong enough
3. the next proof step must improve real-only corpus quality, not just downstream ranking logic
