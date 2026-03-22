# Frozen Blind Run Comparison v1

Date: March 22, 2026

## Purpose

Compare the first true mixed-corpus blind run against the existing curated
historical calibration cases.

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

### What the new mixed run proves

1. The system can now pass a real mixed-corpus blind run on universe discovery.
2. This is stronger evidence than the earlier curated calibrations alone.
3. The mixed run is no longer just:
   - case-selected replay work

### What it still does not prove

1. The mixed run still lags the curated cases on expression specificity.
2. The entity freeze surfaced real names, but final-expression recovery remains
   weak once synthetic-only names are removed.
3. So the system is still better at:
   - pressure-universe formation
   than at:
   - final expression selection

## Second True Mixed Run Status

Status:
- `not executed`

Reason:
1. There is no second frozen historical mixed corpus currently stored under
   [research/archive](/Users/danielschmidt/dev/MiroFish/research/archive).
2. The photonics and memory materials on disk are:
   - calibration memos
   - claim audits
3. They are not frozen source archives suitable for an honest second mixed
   blind run.

## Judgment

Current best read:

1. the project has crossed the threshold from:
   - curated-case promise
   to:
   - one real mixed-corpus blind-pass on universe discovery
2. it has **not** yet crossed the threshold to:
   - proven final-expression discovery

That is real progress.

It is still not the full goal.
