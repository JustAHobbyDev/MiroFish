# Trade Press Prefilter v3 Delta Audit

- Source batches:
  - `trade_press_prefilter_v2`
  - `trade_press_prefilter_v3`
- Changed articles reviewed: `7`

## Summary

- `correct_candidate`: `5`
- `borderline_should_review`: `2`
- `false_positive`: `0`

Overall judgment:
The `trade_press` prefilter patch fixed the main recall problem. It recovered five clearly valid capital-flow candidates and surfaced two planning/load-growth items that belong in `review`.

## Changed Articles

### Correct Candidates

1. `ABB to invest $120M in US manufacturing`
   - `review -> keep`
   - Judgment: `correct_candidate`
   - Why: direct manufacturing investment tied to growing demand.

2. `Rolls-Royce invests $75M in South Carolina engine plant`
   - `drop -> keep`
   - Judgment: `correct_candidate`
   - Why: direct plant expansion tied to data-center demand.

3. `Rockwell Automation confirms Wisconsin factory location, part of $2B US expansion`
   - `drop -> keep`
   - Judgment: `correct_candidate`
   - Why: explicit new factory plus large-scale expansion commitment.

4. `Hitachi unveils $1B grid manufacturing investment, including Virginia transformer factory`
   - `drop -> keep`
   - Judgment: `correct_candidate`
   - Why: direct manufacturing investment and transformer factory buildout.

5. `Schneider Electric to invest $700M in US manufacturing`
   - `drop -> keep`
   - Judgment: `correct_candidate`
   - Why: direct facility expansion and investment tied to infrastructure and data-center demand.

### Borderline Review

6. `PG&E data center pipeline swells to 10GW`
   - `drop -> review`
   - Judgment: `borderline_should_review`
   - Why: strong future-demand and connection-pipeline signal, but still one step upstream of direct buildout.

7. `DTE inks first data center deal to grow electric load 25%`
   - `drop -> review`
   - Judgment: `borderline_should_review`
   - Why: strong load-growth and investment-pipeline context, but not yet a clean direct capital-deployment artifact.

## Model Behavior

### `openai / gpt-4o-mini`

- promoted all `5` recovered keep-items as candidates
- also promoted `PG&E data center pipeline swells to 10GW`

Interpretation:

- good recall
- still somewhat aggressive on `review`-stage planning/load-growth items

### `groq / openai/gpt-oss-20b`

- promoted `3` of the recovered keep-items
- promoted `0` review items
- still showed high schema-failure rate on this batch

Interpretation:

- stricter on review items
- currently too unreliable structurally to serve as the sole reference model here

## Conclusion

The source-class-specific prefilter patch was correct.

For `trade_press`:

1. `investment + factory/plant/manufacturing` should remain surfaced as `keep`
2. `pipeline/load-growth` should remain surfaced as `review`
3. `trade_press` now looks stronger than both `company_release` and broad government feeds for early structural-pressure discovery
