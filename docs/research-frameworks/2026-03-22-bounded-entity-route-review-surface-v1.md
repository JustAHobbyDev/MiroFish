# Bounded Entity Route Review Surface v1

Purpose:
- show public-filing-backed and private-company-backed entities together
- preserve lane boundaries
- preserve route differences

Rules:
1. Input is one or more route-priority batches.
2. Output is a single review surface with:
   - `rows`
   - `rows_by_lane`
   - lane-level metrics
3. Public and private rows stay explicitly labeled:
   - `supported_public_filing`
   - `supported_private_company`
4. Sorting favors:
   - public supported
   - then private supported
   - then priority tier
   - then score

Boundary:
- this is a review and ranking surface
- it does not merge routes
- it does not create new lanes

