# Public Market Scan Candidate v1

Date: March 22, 2026

## Purpose

Turn `ready_for_market_research` public rows into deterministic candidate rows
that match the existing market-pick pipeline shape.

This layer emits:

1. `rows`
2. in the same broad structure already consumed by:
   - [generate_market_picks.py](/Users/danielschmidt/dev/MiroFish/scripts/generate_market_picks.py)

## Important Boundary

This layer is deterministic and role-aware.

It does not pretend the output scores are live market truth.

It provides:

1. a bounded downstream starting point
2. a consistent schema for later screening and pick ranking

## Current Artifact

- [mixed_public_market_scan_candidates_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_public_market_scan_candidates_v1.json)
