# Trade Press Energy Flow V11 Audit

Date: 2026-03-21

## Inputs
- Prefilter batch: `research/archive/normalized/trade_press/trade_press_prefilter_v5_30.json`
- Extractor output: `research/archive/normalized/trade_press/trade_press_energy_flow_gpt4omini_v11_30.json`
- Provider: `openai`
- Model: `gpt-4o-mini`

## Metrics
- Artifacts sent to LLM: `30`
- Successful extractions: `30`
- Schema failures: `0`
- Runtime failures: `0`
- Produced-candidate artifacts: `26`
- No-candidate artifacts: `4`
- Review artifacts: `13`
- Review artifacts promoted: `11`
- Total candidates: `51`

## Candidate Audit
- `correct_candidate`: `26`
- `borderline_should_review`: `0`
- `false_positive`: `0`

The surviving candidate set is coherent for the energy-flow lane.

### Correct keep-derived candidates
- Schneider Electric to invest $700M in US manufacturing
- ABB to invest $120M in US manufacturing
- GE Vernova to invest nearly $600M in US factories
- Rolls-Royce invests $75M in South Carolina engine plant
- Mitsubishi Electric subsidiary invests $86M in switchgear factory
- Rowan Digital breaks ground on 300MW data center campus outside San Antonio, Texas
- CyrusOne breaks ground on Fort Worth data center campus in Texas
- EdgeCore expands Mesa data center campus in Arizona
- EdgeCore begins construction at 114MW Northern Virginia campus
- EdgeCore secures $235 million in ABS financing
- Rowan secures $500m for 300MW Texas data center project
- Eaton invests $340M in US transformer production
- Schneider Electric to invest $700M in US manufacturing
- Hitachi unveils $1B grid manufacturing investment, including Virginia transformer factory
- As load grows, Southern raises spending plan to $81B

### Correct review-derived candidates
- Power enclosure maker AVL to establish its first US plant
- PG&E data center pipeline swells to 10GW
- US utility Exelon reports data center pipeline of 33GW
- First Energy data center pipeline surges to 2.6GW by 2029
- PPL Electric's data center pipeline soars to 14GW
- Hitachi Energy commits $250M to address transformer shortage
- DTE inks first data center deal to grow electric load 25%
- Exelon data center pipeline jumps to 17 GW as load forecast turns positive
- FirstEnergy’s 5-year data center pipeline doubles to 3 GW
- FirstEnergy expects peak load to grow 45% by 2035 on data centers
- Italy-based Westrafo to build its first US transformer plant

## Rejection Audit
- `correct_rejection`: `4`
- `false_negative`: `0`

### Correct non-candidates
- Rockwell Automation confirms Wisconsin factory location, part of $2B US expansion
- Roche to expand, open Indianapolis and North Carolina sites
- Jabil picks North Carolina for $500M AI facility
- Hyundai boosts US investments to $26B through 2028

These remain valid capital-flow artifacts, but they are not strong enough as energy-flow artifacts because the artifact text lacks explicit:
- energy-system linkage
- or direct data-center buildout linkage

## Decision
- Not all review articles should promote in the energy-flow lane.
- Review-stage utility/load and power-equipment articles do belong in the energy-flow lane.
- Generic industrial expansion should not promote unless the artifact itself contains explicit energy-system or direct data-center buildout linkage.
