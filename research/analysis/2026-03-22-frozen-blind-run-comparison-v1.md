# Frozen Blind Run Comparison v1

Date: March 22, 2026

## Purpose

Compare the first true mixed-corpus blind run against the existing curated
historical calibration cases after synthetic cleanup.

## Facts

### Case 1

`first_frozen_mixed_blind_run_power_v1`

1. type:
   - `true_mixed_corpus_blind_run`
2. universe discovery:
   - `blind_pass`
3. promotion-ready bounded universes:
   - `3`
4. final expression:
   - `not_proven`
5. entity surfacing:
   - `partial_pass`

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

### What the mixed run now proves

1. The system still passes a real mixed-corpus blind run on universe discovery.
2. The entity surface can now be evaluated on real-only evidence.
3. This is stronger evidence than the earlier curated calibrations alone.

### What it still does not prove

1. The mixed run still lags the curated cases on expression specificity.
2. Even after synthetic cleanup, the constrained supplier lane is thin.
3. So the system is still better at:
   - pressure-universe formation
   than at:
   - final expression selection

## Second True Mixed Run Status

Status:
- `not executed`

Reason:
1. A second historical mixed corpus now exists.
2. But the current HBM and photonics corpora are retrospective-seeded.
3. They are useful for comparison and stress testing, not yet honest frozen blind runs.

## Judgment

Current best read:

1. the project has crossed the threshold from:
   - curated-case promise
   to:
   - one real mixed-corpus blind-pass on universe discovery
2. it has **not** yet crossed the threshold to:
   - proven final-expression discovery

That remains the correct top-line read after synthetic cleanup.
