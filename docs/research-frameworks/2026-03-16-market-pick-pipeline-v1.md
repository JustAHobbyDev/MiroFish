# Market Pick Pipeline V1

Date: March 16, 2026

## Goal

This pipeline is the reset toward what actually matters:

- scan candidate bottleneck theses
- force a final expression choice
- produce ranked picks

The output is not an ontology or a memo. The output is a pick list with one of:

- `shares`
- `leaps_call`
- `reject`

## Pipeline

1. `Generate candidates`
   Start from expanding markets where bottlenecks plausibly matter:
   - AI photonics
   - HBM / packaging
   - grid equipment
   - rare earths
   - cooling

2. `Score structural mispricing`
   For each candidate, score:
   - hiddenness
   - recognition gap
   - catalyst clarity
   - propagation asymmetry
   - duration mismatch
   - evidence quality

   For names where hidden-supplier asymmetry matters, optionally add:
   - ecosystem centrality
   - downstream valuation gap
   - microcap rerating potential

3. `Score expression quality`
   Score both:
   - `options_fit`
   - `stock_fit`

4. `Force expression choice`
   The current rules are:
   - reject if mispricing score is too low
   - choose `shares` if stock fit clearly beats options fit
   - choose `leaps_call` if options fit clearly beats stock fit
   - otherwise reject

5. `Rank picks`
   Rank by:
   - mispricing score
   - best expression score
   - asymmetry bonus
   - expression bonus / penalty

## Artifacts

Template:

- [market-scan-candidate-template.json](/home/d/codex/MiroFish/research/templates/market-scan-candidate-template.json)

Generator:

- [generate_market_picks.py](/home/d/codex/MiroFish/scripts/generate_market_picks.py)

Example:

```bash
python3 scripts/generate_market_picks.py \
  research/templates/market-scan-candidate-template.json \
  --output-json research/analysis/market-picks-v1.json
```

## Why This Is Closer To The Real Goal

This is designed to answer:

- what are the best current picks?
- should they be expressed in stock or LEAPS?

It is explicitly not trying to optimize for research elegance.

## Current Limitation

This pipeline still depends on human-generated candidate rows.

So today it is a:

- `ranker and picker`

not yet a:

- `full market crawler`

The next gap to close is candidate generation breadth, not more downstream
analysis infrastructure.
