# Second Historical Mixed Corpus HBM Assessment v1

Date: March 22, 2026

## Purpose

Record the build result for the second historical mixed corpus centered on HBM
and advanced packaging.

## Facts

### Corpus manifest

- [second-historical-mixed-corpus-hbm-v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/manifests/second-historical-mixed-corpus-hbm-v1.json)

### Raw collected output

- [second_historical_mixed_corpus_hbm_raw_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/raw/historical_mixed/second_historical_mixed_corpus_hbm_raw_v1.json)

### Raw corpus counts

1. manifest entries:
   - `9`
2. fetched entries:
   - `7`
3. fetch failures:
   - `2`
4. raw source-class mix:
   - `company_release`: `5`
   - `company_filing`: `2`

### Fetch failures

1. `sandisk_ultraqlc_2025_08_05`
   - `TimeoutError`
2. `sandisk_kioxia_fab2_2025_09_29`
   - `HTTP 404`

### Prefilter output

- [second_historical_mixed_corpus_hbm_prefilter_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/second_historical_mixed_corpus_hbm_prefilter_v1.json)

Counts:

1. kept:
   - `1`
2. review:
   - `0`
3. dropped:
   - `6`

The only current keep is:

1. `Micron Breaks Ground on New HBM Advanced Packaging Facility in Singapore`

## Assessment

### What succeeded

1. The repo now contains a second real historical mixed corpus.
2. It is based on fetched primary-source pages, not only memo text.
3. It preserves mixed source classes:
   - company releases
   - company filings

### Important boundary

This corpus is **not** blind-ready.

Why:
1. it is seeded from previously identified public-evidence packs
2. it is not collected from a broad pre-registered source universe
3. government source coverage is missing because commerce.gov blocked
   programmatic fetches

### Why the prefilter looks thin

The raw corpus is more valuable than the first-pass prefilter count suggests.

Reason:
1. the current capital-flow prefilter is tuned for event-form first-pass
   discovery
2. the filing pages in this corpus are mostly corroborating materials, not
   event-form capital-flow headlines

So:
1. the corpus build is a real pass
2. the corpus is not yet a strong first-pass capital-flow batch by itself

## Decision

Current read:

1. second historical mixed corpus:
   - `built`
2. second true blind-run corpus:
   - `not yet`

This is a usable historical source pack for later replay and comparison work.
