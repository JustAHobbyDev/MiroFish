# Third Historical Mixed Corpus Photonics Anchor-First Replay v1

Date: March 22, 2026

Inputs:

- [third_historical_mixed_corpus_photonics_prefilter_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/third_historical_mixed_corpus_photonics_prefilter_v1.json)
- [third_historical_mixed_corpus_photonics_anchor_expressions_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/historical_mixed/third_historical_mixed_corpus_photonics_anchor_expressions_v1.json)
- [2026-03-22-photonics-dependency-graph-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-22-photonics-dependency-graph-v1.json)

## Facts

1. Anchor-first surfacing produces `3` real photonics expressions from the historical corpus:
- `Lumentum`
- `Coherent`
- `JX Advanced Metals`

2. Role mix:
- `anchor_expression`: `1`
- `adjacent_anchor`: `1`
- `upstream_dependency`: `1`

3. Replay judgment:
- `anchor_clue_detection`: `pass`
- `adjacent_expression_surfacing`: `pass`
- `upstream_dependency_surfacing`: `pass`
- `hidden_chokepoint_recovery`: `fail`

## Interpretation

1. The anchor-first workflow improves the measured result materially versus the older bottleneck-first framing.
2. It surfaces:
- the visible anchor:
  - `Lumentum`
- the adjacent photonics expression:
  - `Coherent`
- an upstream materials clue:
  - `JX Advanced Metals`

3. It still does not recover the actual hidden chokepoint expression:
- `AXT`

## Why `AXT` still fails

Facts:

1. The corpus remains retrospective-seeded and not blind-ready.
2. The AXT filing entries in the manifest were not collected:
- SEC fetches returned `403`
3. So the replay lacks direct AXT evidence.

Conclusion:

- this replay supports the `anchor -> adjacency -> upstream` workflow hypothesis
- it does not prove final-expression recovery

## Practical Read

What improved:

1. The system can now surface the kind of starting clue AleaBito appears to have used:
- `LITE`-type anchor

What remains unproven:

1. whether the system can move from that anchor to the actual best hidden upstream expression from real, in-window evidence without retrospective seeding
