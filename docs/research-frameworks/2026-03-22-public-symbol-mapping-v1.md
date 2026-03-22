# Public Symbol Mapping v1

Date: March 22, 2026

## Purpose

Turn `public_investable_now` bounded market handoff rows into a deterministic
 public-market symbol mapping layer.

This layer is intentionally conservative.

It only maps a public symbol when the current repo already contains explicit or
structurally reliable evidence from:

1. live issuer-resolution artifacts
2. official filing collection URLs

## Inputs

Primary input:

- [mixed_bounded_market_handoff_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_bounded_market_handoff_v1.json)

Supporting inputs:

- issuer-resolution live batches
- filing-collection batches

## Output Statuses

1. `mapped_public_symbol`
2. `mapped_foreign_public_symbol`
3. `public_symbol_followup_required`
4. `public_symbol_followup_required_foreign_route`

## Allowed Mapping Bases

1. official SEC lookup URL query parameter such as `CIK=FE`
2. official company or IR note such as `(NYSE: ETN)`
3. official IR stock-code note such as `stock code 6503`
4. official SEC filing document URL patterns such as `exc-20251231.htm`

## Important Boundary

This layer should not guess symbols from memory.

If the repo does not already contain a reliable mapping basis, the correct
output is a follow-up-required status, not a guessed ticker.

## Current Artifact

- [mixed_public_market_symbol_mapping_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_public_market_symbol_mapping_v1.json)
