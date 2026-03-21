# Mixed Corporate Family Candidates v1 Assessment

Date: March 21, 2026

## Facts

1. `mixed_corporate_family_candidates_v1.json` contains `34` family candidates.
2. The conservative normalization rule only merged explicit prefix-family cases.
3. In the transformer lane, the only actual merge was:
   - `Hitachi`
   - `Hitachi Energy`
   into:
   - `Hitachi Energy`

## Decision

1. The conservative merge rule is good enough for the first downstream pass.
2. It removes the concrete duplication we already observed.
3. It does not overreach into speculative aliasing.

## Remaining Boundary

1. `GE Vernova` stays separate.
2. `Westrafo` stays separate.
3. `Mitsubishi Electric` does not appear in the first filing-expansion set because it was not selected in the prior transformer-lane assessment.

