# Trade Press Sample Comparison

- Source batch:
  - `trade_press_sample_prefilter_v1`
- Raw sample:
  - `6` curated articles
- Prefilter result:
  - `2` keep
  - `3` review
  - `1` drop

## Model Comparison

### `openai / gpt-4o-mini`

- `5` artifacts sent
- `3` successful extractions
- `1` candidate artifact
- `2` no-candidate artifacts
- `2` schema failures
- `0 / 3` review artifacts promoted

Observed promoted artifact:

- `Hitachi Energy plans new transformer factory and plant expansions to meet grid demand`

### `groq / openai/gpt-oss-20b`

- `5` artifacts sent
- `4` successful extractions
- `3` candidate artifacts
- `1` no-candidate artifact
- `1` schema failure
- `1 / 3` review artifacts promoted

Observed promoted artifacts:

- `Hitachi Energy plans new transformer factory and plant expansions to meet grid demand`
- `Developer starts construction on 250MW AI data center campus with liquid cooling`
- `Schneider Electric to invest $700M in U.S. operations as AI and energy demand rise`

## Takeaway

`trade_press` appears more promising than broad government feeds and less issuer-shaped than `company_release`.

The current sample suggests:

1. explicit construction and factory expansion stories are reliable candidate material
2. investment-focused review items can promote cleanly
3. partnership-only trade-press stories remain appropriate review/no-candidate cases

This makes `trade_press` the strongest next source class for larger-batch testing in the current workflow.
