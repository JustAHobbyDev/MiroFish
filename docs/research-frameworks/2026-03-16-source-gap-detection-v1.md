# Source Gap Detection v1

## Purpose

Make promotion blockers explicit.

This layer answers:

- why a parse has not promoted
- which graduation gates are still failing
- which source classes are required to close those gates
- what the next evidence jobs should be

## Implementation

Primary logic:

- [source_registry.py](/home/d/codex/MiroFish/backend/app/services/source_registry.py)

CLI entry point:

- [analyze_source_gaps.py](/home/d/codex/MiroFish/scripts/analyze_source_gaps.py)

## Output Shape

Each report includes:

- `graduation_status`
- `next_promotion_target`
- `blocking_gates`
- `gap_flags`
- `required_source_classes`
- `target_companies`
- `targeted_next_steps`

The intended use is:

1. run structural parse
2. run graduation
3. run source acquisition plan
4. run source gap report
5. ingest the missing evidence classes
6. rerun the parse and graduation

## Current Examples

- [robotics actuation source gap report](/home/d/codex/MiroFish/research/analysis/2026-03-16-robotics-actuation-source-gap-report-v1.json)
- [SIVE photonics source gap report](/home/d/codex/MiroFish/research/analysis/2026-03-16-sive-photonics-source-gap-report-v1.json)

## Useful Contrast

`robotics_actuation`:

- still `exploratory_only`
- blocked on `source_gate` and `high_conviction_source_gate`
- needs a broad corroboration mix:
  - policy
  - industrial-base funding
  - company filings
  - supplier disclosures
  - foreign filings
  - industry validation
  - expression validation

`sive_photonics`:

- already `watchlist_candidate`
- only blocked on `high_conviction_source_gate`
- needs narrower upgrades:
  - industry-body validation
  - technical-conference confirmation
  - expression-quality evidence

That contrast is exactly the point of this layer: it tells us whether a thesis needs broad structural corroboration or just a few remaining upgrades before promotion.
