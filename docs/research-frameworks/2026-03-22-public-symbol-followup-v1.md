# Public Symbol Follow-Up v1

Date: March 22, 2026

## Purpose

Keep blocked public names on an explicit symbol-resolution path after market
handoff and role classification.

Current important cases:

1. `Rolls-Royce`
2. `Hitachi Energy / Hitachi, Ltd.`

## Follow-Up Types

1. `foreign_public_symbol_followup`
2. `parent_public_symbol_followup`
3. `public_symbol_followup`

## Current Artifact

- [mixed_public_symbol_followup_v1.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/mixed_source/mixed_public_symbol_followup_v1.json)

## Input Policy

- Accept one or more public symbol-mapping batches.
- Combine blocked public rows into one deterministic follow-up queue.
