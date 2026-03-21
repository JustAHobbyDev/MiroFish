# Trade Press Candidate Audit

- Source batches:
  - `trade_press_gpt4omini_v2`
  - `trade_press_gptoss20b_v2`
- Source prefilter batch:
  - `trade_press_prefilter_v2`
- Unique candidate artifacts reviewed: `3`

## Summary

- `correct_candidate`: `3`
- `borderline_should_review`: `0`
- `false_positive`: `0`

Overall judgment:
The extracted candidate set from the surviving `trade_press` artifacts was clean. The main failure in this batch is prefilter recall, not extraction quality.

## Reviewed Artifacts

1. `trade_press_ff46b7dab1b827b4`
   - Title: `Rowan Digital breaks ground on 300MW data center campus outside San Antonio, Texas`
   - Label: `correct_candidate`
   - Note: Direct construction and large committed capital deployment for data center infrastructure.
2. `trade_press_300902f748d55918`
   - Title: `EdgeCore expands Mesa data center campus in Arizona`
   - Label: `correct_candidate`
   - Note: Explicit campus expansion and capacity increase tied to hyperscale demand.
3. `trade_press_c932aca7f0976acc`
   - Title: `ABB to invest $120M in US manufacturing`
   - Label: `correct_candidate`
   - Note: Direct manufacturing investment and capacity increase tied to electrification and data-center demand.

## Implication

`trade_press` currently looks stronger than broad government feeds for this workflow when relevant articles survive the deterministic prefilter.
