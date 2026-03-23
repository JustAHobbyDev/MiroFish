# Third Historical Mixed Corpus Photonics Anchor-First Replay v2

Date: March 22, 2026

Inputs:

- [third_historical_mixed_corpus_photonics_prefilter_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/third_historical_mixed_corpus_photonics_prefilter_v2.json)
- [third_historical_mixed_corpus_photonics_anchor_expressions_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/third_historical_mixed_corpus_photonics_anchor_expressions_v2.json)
- [third_historical_mixed_corpus_photonics_anchor_first_replay_v2.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/third_historical_mixed_corpus_photonics_anchor_first_replay_v2.json)
- [2026-03-22-photonics-dependency-graph-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-22-photonics-dependency-graph-v1.json)

## Facts

1. Anchor-first surfacing now produces `4` real photonics expressions:
- `Lumentum`
- `Coherent`
- `AXT`
- `JX Advanced Metals`

2. Role mix:
- `anchor_expression`: `1`
- `adjacent_anchor`: `1`
- `upstream_dependency`: `2`

3. Replay judgment:
- `anchor_clue_detection`: `pass`
- `adjacent_expression_surfacing`: `pass`
- `upstream_dependency_surfacing`: `pass`
- `hidden_chokepoint_recovery`: `pass`

## Interpretation

1. Once the real `AXT` filings are present, the anchor-first workflow does recover the named upstream chokepoint.
2. That is strong evidence that the earlier photonics failure was primarily a corpus problem.
3. It is not proof of blind discovery.

## Boundary

This replay still does not justify a full blind-success claim.

Why:

1. the corpus is retrospective-seeded
2. the corpus is still missing at least one relevant source row:
- `Broadcom`
3. the workflow is being tested inside a relevance-selected universe, not a broad historical crawl

## Product Implication

1. The anchor-first workflow is materially more faithful to the AleaBito photonics path than the earlier bottleneck-first framing.
2. The next hard problem is no longer whether `anchor -> adjacency -> upstream` can work in principle.
3. The next hard problem is whether we can collect the real broad corpus that lets it happen without seeded hindsight.
