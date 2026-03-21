# Trade Press Batch v5 / v7 Delta Assessment

## Scope
- Prefilter delta:
  - [trade_press_prefilter_v4_30.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/trade_press/trade_press_prefilter_v4_30.json)
  - [trade_press_prefilter_v5_30.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/trade_press/trade_press_prefilter_v5_30.json)
- OpenAI extraction delta:
  - [trade_press_gpt4omini_v4_30.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/trade_press/trade_press_gpt4omini_v4_30.json)
  - [trade_press_gpt4omini_v7_30.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/trade_press/trade_press_gpt4omini_v7_30.json)

## Facts
- Prefilter `v4 -> v5`
  - `keep`: `15 -> 17`
  - `review`: `12 -> 13`
  - `drop`: `3 -> 0`
- Changed artifacts:
  - `drop -> keep`
    - `Eaton invests $340M in US transformer production`
    - `As load grows, Southern raises spending plan to $81B`
  - `drop -> review`
    - `FirstEnergy expects peak load to grow 45% by 2035 on data centers`

- OpenAI extraction `v4 -> v7`
  - `artifacts_sent_to_llm`: `27 -> 30`
  - `successful_extractions`: `22 -> 24`
  - `schema_failure_count`: `5 -> 6`
  - `produced_candidate_artifact_count`: `22 -> 17`
  - `no_candidate_artifact_count`: `0 -> 7`
  - `review_candidate_artifact_count`: `10 -> 4`

## Changed-Artifact Outcome
- `Eaton invests $340M in US transformer production`
  - `keep`
  - `produced_candidates = true`
- `As load grows, Southern raises spending plan to $81B`
  - `keep`
  - `produced_candidates = true`
- `FirstEnergy expects peak load to grow 45% by 2035 on data centers`
  - `review`
  - `produced_candidates = false`
  - heuristic rejection applied

## Review-Stage Utility Pressure Outcome
- Forced to `no_candidate`:
  - `PG&E data center pipeline swells to 10GW`
  - `US utility Exelon reports data center pipeline of 33GW`
  - `First Energy data center pipeline surges to 2.6GW by 2029`
  - `PPL Electric's data center pipeline soars to 14GW`
  - `Exelon data center pipeline jumps to 17 GW as load forecast turns positive`
  - `FirstEnergy’s 5-year data center pipeline doubles to 3 GW`
  - `FirstEnergy expects peak load to grow 45% by 2035 on data centers`
- Still allowed as candidate:
  - `DTE inks first data center deal to grow electric load 25%`

## Conclusion
- The prefilter gap from the 30-article run is fixed for the audited missed headline classes.
- The review-stage extraction gate is now behaving much closer to the intended boundary:
  - planning-stage utility pipeline and forecast articles stay below candidate status
  - concrete signed-demand and explicit spend/buildout articles still pass
- `trade_press` remains the strongest source class tested so far.

## Open Questions
- Should explicit utility spending-plan articles like Southern remain `keep`, or should they become `review` until the article names concrete project categories?
