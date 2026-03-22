# Narrowed Bounded Universe Adapter v1

## Purpose

Turn a real-only narrowed structural-pressure lane into an exploratory
`bounded_universe_candidate` so it can reuse the existing bounded-universe,
research-set, and entity-candidate pipeline.

## Boundary

This adapter does not make the narrowed lane promotion-ready.
It preserves:

1. `exploratory_candidate`
2. real-only provenance
3. a constrained source scope until broader corroboration exists
