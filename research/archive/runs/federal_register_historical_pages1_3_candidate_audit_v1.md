# Federal Register Candidate Audit

- Source batches:
  - `federal_register_historical_pages1_3_gpt4omini_v3`
  - `federal_register_historical_pages1_3_gptoss20b_v3`
- Source prefilter batch:
  - `federal_register_historical_pages1_3_prefilter_v2`
- Unique candidate artifacts reviewed: `11`

## Summary

- `correct_candidate`: `3`
- `borderline_should_review`: `3`
- `false_positive`: `5`

Overall judgment:
Government candidate extraction remains too permissive on trade-policy and standards notices, but it is surfacing a small number of valid construction and land-opening signals.

## Findings

1. Clean government candidates do exist
   - SMR phased construction permit / limited work authorization
   - public land order opening land to resource development
   - Navy demolition/construction project authorization

2. Policy-enablement notices should usually remain review-stage objects
   - record of decision
   - lease-sale reaffirmation
   - regulation removal that enables construction

3. Trade-policy and standards notices are still a false-positive class
   - antidumping / circumvention determinations
   - spectrum-rule expansions
   - standards approvals
   - permit-objection denials for existing facilities

## Implication

For government feeds:

- `construction / permit / land-opening / direct project authorization` can be valid candidate material
- `planning-enablement` should usually surface to `review`
- `trade-policy / standards-only` should be treated as likely false-positive territory unless paired with more direct buildout evidence
