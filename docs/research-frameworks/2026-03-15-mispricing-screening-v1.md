# Mispricing Screening V1

## Purpose

MiroFish now has a first explicit handoff layer from structural research to a
tradable hypothesis.

The new artifact is a `mispricing candidate`.

It is meant to answer two questions separately:

1. Does this thesis look plausibly underpriced?
2. Are options a sensible expression path for that thesis?

This still does **not** mean MiroFish can price options. It means the system can
now emit a structured shortlist for downstream options work.

## Artifact Shape

Each candidate includes:

- thesis summary
- underlying ticker
- mispricing type
- posture
- preferred expression
- time horizon
- catalysts
- invalidations
- structural reference back to the bottleneck work
- `mispricing_signals`
- `options_expression_signals`

## Scores

The screener emits two score dimensions:

- `mispricing`
  - how plausible it is that the market is underestimating the structural setup
- `options_fit`
  - how plausible it is that options are the right expression path

Both are `0-100` and use the same qualitative bands already used elsewhere:

- `critical`
- `high`
- `moderate`
- `emerging`
- `low`

## Current Limits

This is still upstream screening, not full trade construction.

Not included yet:

- live options chain ingestion
- implied-vol surface checks
- realized-vs-implied comparisons
- liquidity / open-interest validation
- strike selection
- portfolio sizing

## Backend Surface

Persistence:

- `artifacts/mispricing_candidates.json`

Research project API:

- `POST /api/research/project/<research_project_id>/mispricing-candidates`
- `POST /api/research/project/<research_project_id>/mispricing-candidates/screen`

## Immediate Workflow

1. Start from thesis intake, claims audit, and chokepoint scorecards.
2. Define 3-5 candidate expressions.
3. Screen them through the mispricing artifact.
4. Rank by `mispricing` and `options_fit`.
5. Only then hand the shortlist to a real market-data / options layer.

## Why This Matters

This is the shortest credible path to proving or falsifying the core fork thesis:

`Can MiroFish systematically identify option-mispricing candidates from hidden structural dependencies?`
