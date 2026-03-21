# Trade Press Prefilter Drop Audit

- Source batch:
  - `trade_press_prefilter_v2`
- Reviewed scope:
  - all `6` dropped artifacts

## Summary

- `correct_rejection`: `0`
- `borderline_should_review`: `2`
- `false_negative`: `4`

Overall judgment:
The current deterministic prefilter is too narrow for `trade_press`. It under-detects direct investment and factory-expansion stories when the headline lacks one of the current event-form tokens.

## Reviewed Artifacts

1. `Rolls-Royce invests $75M in South Carolina engine plant`
   - Label: `false_negative`
   - Note: Direct investment into plant expansion to meet data center demand. This should not be dropped.
2. `Rockwell Automation confirms Wisconsin factory location, part of $2B US expansion`
   - Label: `false_negative`
   - Note: New factory siting and explicit expansion. This should not be dropped.
3. `PG&E data center pipeline swells to 10GW`
   - Label: `borderline_should_review`
   - Note: Strong future-demand and connection-pipeline signal, but more planning-oriented than direct buildout. This should surface to review.
4. `Hitachi unveils $1B grid manufacturing investment, including Virginia transformer factory`
   - Label: `false_negative`
   - Note: Direct manufacturing investment and factory buildout. This should not be dropped.
5. `Schneider Electric to invest $700M in US manufacturing`
   - Label: `false_negative`
   - Note: Direct investment and facility expansion tied to data-center and infrastructure demand. This should not be dropped.
6. `DTE inks first data center deal to grow electric load 25%`
   - Label: `borderline_should_review`
   - Note: Strong load-growth and investment-pipeline signal, but still one step upstream of direct buildout. This should surface to review.

## Main Finding

For `trade_press`, the current prefilter underweights:

1. `invest` / `investment`
2. `factory`
3. `plant`
4. `pipeline`
5. `load growth`

These should not all become unconditional `keep`, but they should stop defaulting to `drop`.
