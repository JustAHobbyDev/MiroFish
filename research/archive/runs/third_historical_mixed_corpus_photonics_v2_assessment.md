# Third Historical Mixed Corpus Photonics v2 Assessment

Date: March 22, 2026

Inputs:

- [third-historical-mixed-corpus-photonics-v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/manifests/third-historical-mixed-corpus-photonics-v1.json)
- [third_historical_mixed_corpus_photonics_raw_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/raw/historical_mixed/third_historical_mixed_corpus_photonics_raw_v2.json)
- [third_historical_mixed_corpus_photonics_prefilter_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/third_historical_mixed_corpus_photonics_prefilter_v2.json)

## Facts

1. The rebuilt photonics corpus now fetches the real `AXT` filing pages.
- recovered:
  - `axt_10q_2025_03_31_inp_ai`
  - `axt_10k_2024_12_31_export_controls`

2. Corpus coverage improved materially.
- `entry_count`: `6`
- `fetch_failure_count`: `1`

3. The remaining failure is:
- `Broadcom` third-generation CPO release

4. Filing-aware prefilter output is now usable for anchor-first replay.
- `kept_count`: `4`
- `review_count`: `2`
- kept issuers:
  - `AXT`
  - `AXT`
  - `NVIDIA`
  - `Lumentum`
- review issuers:
  - `Coherent`
  - `JX Advanced Metals`

## Interpretation

1. The main photonics corpus blocker was real `AXT` evidence collection, not the anchor-first replay logic.
2. That blocker is now removed.
3. The corpus is still not a true blind-ready universe.

## Why It Is Still Not Blind-Ready

1. The corpus remains retrospective-seeded from already identified relevant evidence.
2. `Broadcom` is still missing.
3. Source diversity is still narrow:
- `company_release`
- `company_filing`

## Practical Read

1. This is now a valid seeded replay corpus for testing whether the anchor-first workflow can move all the way to the named upstream chokepoint.
2. It is not yet a fair blind-discovery benchmark.
