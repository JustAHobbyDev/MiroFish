# Trade Press Batch v4 30 Assessment

## Facts
- raw batch size: `30`
- source split:
  - `Manufacturing Dive`: `10`
  - `Data Center Dynamics`: `10`
  - `Utility Dive`: `10`
- deterministic prefilter:
  - `15 keep`
  - `12 review`
  - `3 drop`
- OpenAI baseline:
  - `27` artifacts sent
  - `22` successful extractions
  - `22` candidate artifacts
  - `0` no-candidate
  - `5` schema failures
  - `10/12` review artifacts promoted
- Groq challenger:
  - `27` artifacts sent
  - `11` successful extractions
  - `11` candidate artifacts
  - `0` no-candidate
  - `16` schema failures
  - `5/12` review artifacts promoted

## Audit Results
- candidate union audit:
  - `25` artifact candidates
  - `18` `correct_candidate`
  - `7` `borderline_should_review`
  - `0` `false_positive`
- review audit:
  - `12` review artifacts
  - `5` valid candidates
  - `7` should remain review-stage
- drop audit:
  - `3` dropped artifacts
  - `2` clear false negatives
  - `1` borderline review item

## Conclusions
- `trade_press` remains the strongest source class tested for early discovery.
- The prefilter is now directionally correct, but not finished.
- The main remaining prefilter gap is utility and transformer-capex language:
  - `invests ... production`
  - `raises spending plan`
  - `peak load grows`
- `gpt-4o-mini` remains the practical reference extractor for this lane.
- `gpt-oss-20b` is still too schema-unstable for primary use at this batch size.
- The main model-quality issue is not obvious false positives.
- The main model-quality issue is that `gpt-4o-mini` over-promotes some review-stage pipeline and forecast articles into direct candidates.

## Recommendation
1. Patch the `trade_press` prefilter for the three missed headline classes found in the drop audit.
2. Add a narrow post-extraction rule so utility pipeline and load-forecast articles default to `review` unless the artifact contains explicit spend, signed offtake, financing, siting, or construction.
3. Rerun the same 30-article batch after the patch and compare only the changed artifacts first.

## Open Questions
- Should the review-stage utility pipeline articles remain as capital-flow candidates in a later `narrowing` workflow, or should they always stay below candidate status until a direct spend/buildout artifact appears?
