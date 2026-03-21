# Trade Press Batch v4 30 Candidate Audit v1

## Scope
- Union of artifact-level candidates surfaced by:
  - `openai/gpt-4o-mini`
  - `groq/openai-gpt-oss-20b`

## Summary
- artifact candidates reviewed: `25`
- `correct_candidate`: `18`
- `borderline_should_review`: `7`
- `false_positive`: `0`

## Main Findings
- `keep` artifacts were almost entirely clean.
- The main disagreement is in the `review` bucket, not the `keep` bucket.
- Utility pipeline and load-growth headlines remain useful, but they are still mostly `review`-stage signals rather than direct capital-flow candidates.
- Both models surfaced valid candidates that the other missed because of schema instability, so model comparison still matters.

## Correct Candidates
- Schneider Electric to invest $700M in US manufacturing
- Rolls-Royce invests $75M in South Carolina engine plant
- Rockwell Automation confirms Wisconsin factory location, part of $2B US expansion
- Mitsubishi Electric subsidiary invests $86M in switchgear factory
- Roche to expand, open Indianapolis and North Carolina sites
- Rowan Digital breaks ground on 300MW data center campus outside San Antonio, Texas
- CyrusOne breaks ground on Fort Worth data center campus in Texas
- EdgeCore expands Mesa data center campus in Arizona
- EdgeCore begins construction at 114MW Northern Virginia campus
- Rowan secures $500m for 300MW Texas data center project
- Schneider Electric to invest $700M in US manufacturing
- Hitachi unveils $1B grid manufacturing investment, including Virginia transformer factory
- Power enclosure maker AVL to establish its first US plant
- DTE inks first data center deal to grow electric load 25%
- Italy-based Westrafo to build its first US transformer plant
- GE Vernova to invest nearly $600M in US factories
- Jabil picks North Carolina for $500M AI facility
- Hitachi Energy commits $250M to address transformer shortage

## Borderline Should Review
- Hyundai boosts US investments to $26B through 2028
- PG&E data center pipeline swells to 10GW
- US utility Exelon reports data center pipeline of 33GW
- First Energy data center pipeline surges to 2.6GW by 2029
- PPL Electric's data center pipeline soars to 14GW
- Exelon data center pipeline jumps to 17 GW as load forecast turns positive
- FirstEnergy’s 5-year data center pipeline doubles to 3 GW

## Conclusion
- The `trade_press` candidate set is high quality.
- The current over-promotion risk is concentrated in utility pipeline and load-growth articles.
- No clear false-positive class appeared in this 30-article run.
