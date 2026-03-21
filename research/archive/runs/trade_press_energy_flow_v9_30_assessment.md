# Trade Press Energy Flow V9 Assessment

Date: 2026-03-21

## Inputs
- Prefilter batch: `research/archive/normalized/trade_press/trade_press_prefilter_v5_30.json`
- Extractor output: `research/archive/normalized/trade_press/trade_press_energy_flow_gpt4omini_v9_30.json`
- Provider: `openai`
- Model: `gpt-4o-mini`

## Metrics
- Artifacts sent to LLM: `30`
- Successful extractions: `29`
- Schema failures: `1`
- Runtime failures: `0`
- Produced-candidate artifacts: `29`
- Review artifacts: `13`
- Review artifacts promoted: `13`
- Total candidates: `56`

## Interpretation
- The energy-flow extraction path is now operational on the full 30-article trade-press batch.
- The main failure mode was schema brittleness around natural model labels, not provider connectivity or prompt breakdown.
- Candidate-level validation with invalid-subcandidate dropping was the decisive fix.
- One remaining alias miss remained in the full batch artifact set, but it was resolved on a targeted one-artifact live retry.

## Final Status
- Treat `trade_press_energy_flow_gpt4omini_v9_30.json` as the current benchmark artifact.
- Treat the remaining gap as minor schema cleanup, not a blocker to continuing the energy-flow lane.
