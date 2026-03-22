# Bounded Entity Downstream State v1

## Purpose
- Consolidate follow-up entities into one deterministic downstream state object after route resolution.

## Inputs
- follow-up queue
- filing support batch
- private-company diligence plan batch

## Output Statuses
- `public_filing_supported`
- `private_company_diligence_required`

## Rules
- If private-company diligence exists for an entity:
  - route to `private_company_diligence_required`
- Else if filing support exists:
  - route to `public_filing_supported`

## Follow-up Status Normalization
- `private_route_resolved`
- `already_supported`
- otherwise preserve the queue status

## Intent
- Keep public-filing and private-company paths in one reviewable downstream object without mixing their evidence sources.
