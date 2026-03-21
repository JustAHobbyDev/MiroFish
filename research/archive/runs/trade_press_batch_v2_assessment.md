# Trade Press Batch v2 Assessment

- Raw batch:
  - `trade_press_batch_v2`
- Prefilter:
  - `trade_press_prefilter_v2`
- Extraction:
  - `trade_press_gpt4omini_v2`
  - `trade_press_gptoss20b_v2`

## Facts

1. Batch size: `9`
2. Prefilter result:
   - `2` keep
   - `1` review
   - `6` drop
3. Candidate audit on surviving set:
   - `3 / 3` unique candidates were correct
4. Drop audit:
   - `4 / 6` drops were false negatives
   - `2 / 6` drops should have been review

## Conclusion

`trade_press` is the strongest source class tested so far for the current workflow, but the shared deterministic prefilter is materially under-recalling it.

This is not an extraction-quality problem.
It is a prefilter recall problem.

## Recommendation

Next patch should be trade-press-specific:

1. route `invest` / `investment` + `factory` / `plant` into `keep` or `review`
2. route `pipeline` / `load growth` / `load increase` into `review`
3. rerun the same `trade_press_batch_v2` and re-audit deltas
