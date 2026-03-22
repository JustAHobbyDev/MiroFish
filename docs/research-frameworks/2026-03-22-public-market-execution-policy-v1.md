# Public Market Execution Policy v1

Date: March 22, 2026

## Purpose

Encode a conservative execution policy from the combined public review surface.

## Policy

1. `default_us_executable`
   - only for actionable rows with direct U.S.-primary symbols
2. `requires_us_secondary_access_review`
   - for actionable rows with foreign-home listings but some U.S. reference
3. `requires_foreign_execution_review`
   - for actionable rows with foreign-home listings and no current U.S. access evidence
4. `blocked_by_pick_reject`
   - for rows that are not currently actionable regardless of listing access

## Current Artifact

- [mixed_public_market_execution_policy_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_public_market_execution_policy_v1.json)
