# Public Picks Event Study Schema V1

Date: March 15, 2026

## Purpose

This schema is for a later reconstruction study of public investing or options
ideas posted by `u/AleaBito` / `@aleabitoreddit`.

The goal is not to recreate exact account PnL. The goal is to evaluate:

- whether the public ideas had forward edge
- what kinds of ideas worked best
- whether the edge came from thesis generation, trade expression, or timing

This schema assumes public posts will often be incomplete, vague, or theatrical.
It is designed to preserve uncertainty instead of forcing false precision.

## Unit Of Analysis

One row should represent one distinct public idea at its first recoverable public
timestamp.

Examples:

- one Reddit post with a clear ticker thesis
- one X thread introducing a specific idea
- one follow-up post only if it materially changes the original expression

Do not create a new row for every comment unless the comment materially changes:

- ticker
- direction
- instrument
- tenor
- strike or moneyness
- invalidation

## Core Principles

1. Record the first public timestamp, not a later viral timestamp.
2. Separate `idea quality` from `trade expression quality`.
3. Grade specificity explicitly.
4. Refuse false precision when the post does not justify it.
5. Benchmark all forward results.

## Schema

### Identity And Source

- `idea_id`
  Stable internal identifier.
- `person`
  Example: `AleaBito`.
- `platform`
  Example: `reddit`, `x`.
- `source_type`
  Example: `post`, `thread`, `comment`.
- `source_url`
  Canonical permalink.
- `source_title`
  Post title or short label.
- `first_public_timestamp_utc`
  Earliest recoverable timestamp for the idea.
- `source_text_excerpt`
  Short excerpt for auditability.

### Instrument And Thesis

- `underlying_symbol`
  Main ticker or asset.
- `related_symbols`
  Optional comma-separated list for baskets or dependency chains.
- `asset_type`
  Example: `equity`, `etf`, `option`, `warrant`, `pair`, `other`.
- `direction`
  Example: `long`, `short`, `long_vol`, `short_vol`, `hedged`, `unclear`.
- `thesis_type`
  Example:
  - `hidden_bottleneck`
  - `valuation_dislocation`
  - `variance_underpricing`
  - `special_situation`
  - `warrant_arbitrage`
  - `discretionary_directional`
- `thesis_summary`
  One- or two-sentence restatement in plain English.
- `stated_catalysts`
  Free-text summary.
- `stated_invalidation`
  Free-text summary.

### Expression Details

- `expression_type`
  Example:
  - `shares`
  - `calls`
  - `puts`
  - `leaps_calls`
  - `leaps_puts`
  - `warrants`
  - `pair_trade`
  - `unknown`
- `tenor_bucket`
  Example:
  - `intraday`
  - `short_dated`
  - `medium_dated`
  - `long_dated`
  - `leaps`
  - `unknown`
- `expiry_date`
  If explicitly stated.
- `strike`
  If explicitly stated.
- `moneyness_hint`
  Example: `atm`, `otm`, `itm`, `far_otm`, `unknown`.
- `entry_hint`
  Free text for any usable entry guidance.
- `exit_hint`
  Free text for any usable exit guidance.

### Specificity And Reconstruction Confidence

- `specificity_grade`
  Required.
  Values:
  - `exact`
  - `partial`
  - `vague`
  - `unusable`

Definitions:

- `exact`
  Enough information to identify the intended instrument or a very tight proxy.
- `partial`
  Underlying and broad expression are clear, but the exact contract or timing is
  not.
- `vague`
  A theme or ticker exists, but not enough to evaluate expression fairly.
- `unusable`
  Too ambiguous to score.

- `reconstruction_confidence`
  `high`, `medium`, `low`.
- `proxy_required`
  `true` or `false`.
- `proxy_definition`
  If a proxy is used, define it explicitly.

### Market Snapshot At Publication

- `underlying_spot_at_post`
- `benchmark_symbol`
  Example: `SPY`, `QQQ`, `SOXX`, `XLI`.
- `benchmark_spot_at_post`
- `sector_context`
  Optional context like `semis`, `materials`, `Korea ETF`, `data center`.

For options ideas when available:

- `front_iv_at_post`
- `target_expiry_iv_at_post`
- `oi_hint_at_post`
- `spread_quality_hint_at_post`

These can be null when unavailable.

### Forward Outcome Windows

For all ideas:

- `ret_5d_pct`
- `ret_1m_pct`
- `ret_3m_pct`
- `ret_6m_pct`
- `ret_12m_pct`

Benchmark-relative versions:

- `alpha_5d_pct`
- `alpha_1m_pct`
- `alpha_3m_pct`
- `alpha_6m_pct`
- `alpha_12m_pct`

For options or proxy-option ideas:

- `proxy_option_ret_1m_pct`
- `proxy_option_ret_3m_pct`
- `proxy_option_ret_6m_pct`
- `proxy_option_ret_12m_pct`

These should only be filled when `specificity_grade` is `exact` or a clearly
defined proxy exists.

### Outcome Classification

- `thesis_outcome`
  Example:
  - `worked`
  - `partially_worked`
  - `failed`
  - `unclear`
- `expression_outcome`
  Example:
  - `good_expression`
  - `bad_expression`
  - `good_idea_bad_timing`
  - `unclear`
- `timing_outcome`
  Example:
  - `good`
  - `acceptable`
  - `poor`
  - `unclear`
- `vega_expansion_observed`
  `true`, `false`, or `unknown`.
- `notes`
  Free-text comments.

## Recommended Evaluation Rules

### Shares / equity ideas

Use first public timestamp to measure:

- absolute forward return
- benchmark-relative forward return
- max move in favor and against if later added

### Options ideas with exact contracts

Measure:

- contract mid-price at post
- contract mid-price at forward windows
- underlying return
- implied volatility change if available

This allows separation of:

- directional correctness
- volatility repricing
- bad entry due to already-rich premium

### Options ideas with partial but not exact detail

Use a predeclared proxy, for example:

- nearest LEAPS call around `10-20 delta`
- nearest LEAPS call around `25-35 delta`
- first listed expiry beyond `9 months`

Do not improvise the proxy after seeing performance.

## Minimum Fields To Preserve Even If Data Is Weak

If the post is too vague for full evaluation, still preserve:

- source URL
- timestamp
- ticker
- broad direction
- thesis summary
- specificity grade

That keeps the historical record useful without pretending precision.

## Suggested Analysis Views

Once data exists, the most useful cuts are:

- by `thesis_type`
- by `expression_type`
- by `specificity_grade`
- by `platform`
- by `time period`

The most important split is:

- `good idea, bad expression`
- `good idea, good expression`
- `bad idea`

## Practical Warning

This study will only be worth doing if enough rows are at least `partial`.

If most public picks are `vague` or `unusable`, the conclusion should be:

- the public record is not sufficient for a fair event study

That is still a useful answer.

## Calibration Note

`AleaBito` should be treated as a calibration benchmark, not as ground truth.

The intended use is:

- if the system consistently rejects his strongest ideas, that is a warning
- if the system agrees with the thesis but disagrees with the expression, that
  may still be correct
- if the system merely imitates every public pick, that is also a warning

The best future evaluation questions are:

- does the system recognize why his strongest ideas are interesting
- does it avoid weak or over-expensive expressions
- can it surface adjacent or cleaner expressions from the same dependency chain

So the benchmark is not `perfect agreement`. The benchmark is `useful
alignment on high-quality ideas without collapsing into imitation`.
