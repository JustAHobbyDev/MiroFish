# Trade Press Batch v3 Assessment

- Prefilter:
  - `trade_press_prefilter_v3`
- Extraction:
  - `trade_press_gpt4omini_v3`
  - `trade_press_gptoss20b_v3`

## Facts

1. Prefilter result:
   - `7` keep
   - `2` review
   - `0` drop

2. Delta audit on newly recovered articles:
   - `5` correct candidates
   - `2` borderline review items

3. `openai / gpt-4o-mini`
   - `7` successful extractions
   - `7` candidate artifacts
   - `1 / 2` review artifacts promoted

4. `groq / openai/gpt-oss-20b`
   - `3` successful extractions
   - `3` candidate artifacts
   - `0 / 2` review artifacts promoted
   - `6` schema failures

## Conclusion

The prefilter patch fixed the main trade-press recall problem.

`trade_press` is now the strongest source class tested so far for the current workflow:

1. broad enough for early discovery
2. cleaner than broad government feeds
3. less issuer-shaped than company releases

## Recommendation

1. treat `trade_press` as the primary next source class for larger-scale testing
2. keep `openai / gpt-4o-mini` as the current reference extractor for this lane
3. keep `gpt-oss-20b` as a challenger only until schema reliability improves
