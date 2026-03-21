# Trade Press Batch v7 Candidate Audit v1

## Summary
- candidate artifacts reviewed: `17`
- `correct_candidate`: `17`
- `borderline_should_review`: `0`
- `false_positive`: `0`

## Facts
- This audit covers the final tightened OpenAI run:
  - [trade_press_gpt4omini_v7_30.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/trade_press/trade_press_gpt4omini_v7_30.json)
- The previously problematic review-stage utility pipeline and load-forecast articles are no longer in the candidate set.
- Remaining candidate artifacts are either:
  - direct spend / manufacturing expansion
  - direct construction / campus buildout
  - concrete signed-demand or shortage-response articles

## Correct Candidates
- Schneider Electric to invest $700M in US manufacturing
- ABB to invest $120M in US manufacturing
- Rolls-Royce invests $75M in South Carolina engine plant
- Rockwell Automation confirms Wisconsin factory location, part of $2B US expansion
- Mitsubishi Electric subsidiary invests $86M in switchgear factory
- Roche to expand, open Indianapolis and North Carolina sites
- Rowan Digital breaks ground on 300MW data center campus outside San Antonio, Texas
- EdgeCore expands Mesa data center campus in Arizona
- EdgeCore begins construction at 114MW Northern Virginia campus
- Eaton invests $340M in US transformer production
- Schneider Electric to invest $700M in US manufacturing
- Hitachi unveils $1B grid manufacturing investment, including Virginia transformer factory
- As load grows, Southern raises spending plan to $81B
- Power enclosure maker AVL to establish its first US plant
- Hitachi Energy commits $250M to address transformer shortage
- DTE inks first data center deal to grow electric load 25%
- Italy-based Westrafo to build its first US transformer plant

## Conclusion
- The final `v7` candidate set is clean for the current workflow.
- The remaining quality problem on this benchmark is not false positives.
- The remaining quality problem is schema instability on a handful of valid artifacts.

## Open Questions
- Should duplicate valid artifacts like the two Schneider captures be deduped before candidate audit metrics are computed, or should the benchmark continue to treat them as separate artifact-level successes?
