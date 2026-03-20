# AleaBito Methods Archaeology v1

Date: March 19, 2026

Purpose:

- mine AleaBito's X archive for context around how expressions were constructed
- separate `what he picked` from `how he said he got there`
- identify recurring source classes, method language, and validation steps around `AXTI` and `SNDK`

Primary inputs:

- [aleabitoreddit-daily-archive-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/aleabitoreddit-daily-archive-v1.json)
- [extract_x_expression_context.py](/Users/danielschmidt/dev/MiroFish/scripts/extract_x_expression_context.py)
- local derived context file: `research/analysis/aleabitoreddit-expression-context-v1.json`

## Facts

### 1. `AXTI` and `SNDK` were not described the same way

`AXTI` context is dominated by:

- `thesis`
- `supply chain`
- `research`
- `earnings`
- `SMM`
- `capacity`
- `DD`
- `price hikes`
- `mapping`

`SNDK` context is dominated by:

- `earnings`
- `price hikes`
- `capacity`
- `research`
- `supply chain`
- `thesis`

Implication:

- `AXTI` looks like a supply-chain discovery and bottleneck-mapping expression
- `SNDK` looks more like a cycle-level operating-leverage expression that gets validated by pricing, earnings, and guidance

### 2. AleaBito explicitly talks about `information synthesis`

Examples:

- `2026-01-07` on `AXTI`:
  - "most of my posts from `$AXTI` ... are novel information synthesis based on public info"
- `2026-01-21` on `SNDK`:
  - "I try and discover alpha to find the next `$30->$453 $SNDK` at the start"

Implication:

- he is not presenting the edge as private information
- he is presenting it as earlier synthesis of scattered public information

### 3. He repeatedly references external source classes

Named or visible source types in the archive include:

- company earnings reports
- earnings calls
- CEO quotes
- analyst notes
- analyst estimates
- supply-chain research
- price databases
- trade publications / industry researchers

Named examples:

- `SMM`
- `SemiAnalysis`
- `Trendforce`
- `Morgan Stanley`
- `Digitimes`
- `Lightcounting`
- `Northland`
- `Benchmark`
- `Needham`
- `Craig-Hallum`
- `Phison CEO interview`

### 4. He uses both primary-like and secondary-like evidence

Primary-like:

- earnings reports
- earnings calls
- company capacity raises
- CEO comments
- customer / supplier relationship statements

Secondary-like:

- analyst notes
- industry reports
- pricing trackers
- press summaries
- comments from domain specialists on X

Implication:

- the process is not pure primary-source investing
- it is a mixed synthesis stack with public secondaries feeding the early map

## `AXTI` Methods Trace

### What shows up in the archive

Recurring language:

- "bottom of the entire supply chain"
- "research note"
- "working on a model"
- "market research"
- "single point of failure"
- "Northland ... $100M to fund InP substrate expansion"
- "7N prices on SMM have reached ATHs"
- "CEO says 40% of InP supply chain"

Representative context:

- `2025-12-28`:
  - "working on a model to normalize ownership of indium phosphide"
- `2025-12-29`:
  - "from my own personal research so far"
- `2025-12-29`:
  - "`AXTI` CEO - 'We are 40% of the Indium Phosphide supply chain'"
- `2026-01-02`:
  - "market research is showing InP and optical components to become analogous to the HBM shortage"
- `2026-01-03`:
  - "Paywalled info showed ... InP price hikes"
- `2026-01-07`:
  - "lot of things have changed since the last earnings call"
- `2026-01-08`:
  - "most analysts ... model this wrong since it's not linear"

### What this suggests

`AXTI` appears to come from:

1. downstream beneficiary discovery
2. supply-chain deepening
3. upstream concentration mapping
4. feedstock / substrate pricing confirmation
5. financing / capacity-expansion confirmation
6. public narrative publication

This is a bottleneck-discovery workflow.

### Likely source stack for `AXTI`

- supplier/customer relationship mapping
- earnings-call deltas
- CEO statements
- capital raise / expansion news
- Chinese feedstock pricing via `SMM`
- analyst notes for counterarguments
- own internal model of supply ownership and concentration

## `SNDK` Methods Trace

### What shows up in the archive

Recurring language:

- "memory supercycle"
- "price hikes"
- "gross margin expansion"
- "earnings looks like a blowout"
- "reported Q3 guide"
- "Kioxia and Sandisk ... manufacturing sites"
- "analysts were projecting no growth"
- "capacity expansion slow"

Representative context:

- `2026-01-25`:
  - Samsung NAND price hike post citing `ETNews` and `Trendforce`
- `2026-01-29`:
  - Sandisk manufacturing / supply post tied to `Kioxia`
- `2026-01-29`:
  - explicit earnings beat versus estimates
- `2026-02-15`:
  - "analysts were projecting no growth, but hoarding from AI demand likely triples revenue estimates"
- `2026-02-16`:
  - `Phison CEO interview` and "intentionally keeping capacity expansion slow"

### What this suggests

`SNDK` appears to come from:

1. broad memory-cycle recognition
2. pricing shock observation
3. valuation mismatch versus revised economics
4. earnings/guidance confirmation
5. second-order beneficiary mapping

This is a cycle-expression workflow more than a hidden-chokepoint workflow.

### Likely source stack for `SNDK`

- NAND / DRAM pricing reports
- earnings and guidance
- partner manufacturing disclosures
- management / industry interviews
- sell-side estimate mismatch
- market-underreaction to revised profitability

## Comparative Read

### `AXTI`

Best described as:

- `upstream bottleneck mapping`

Core evidence shape:

- structural concentration
- supply-chain position
- capacity / price pressure
- customer dependence

### `SNDK`

Best described as:

- `cycle profitability and expression selection`

Core evidence shape:

- memory pricing regime shift
- earnings power repricing
- estimate mismatch
- operating leverage within a known cycle

## Strongest Current Hypothesis

The archive suggests AleaBito does not use one single method for every expression.

Instead, he appears to combine at least two related workflows:

1. `bottleneck discovery`
   - best fit for `AXTI`
   - driven by supply-chain mapping, concentration, and hidden upstream importance

2. `cycle expression selection`
   - best fit for `SNDK`
   - driven by pricing, earnings power, and market-underestimated operating leverage

Both still sit inside the broader pattern of:

- public information synthesis
- structural mapping
- early expression selection before consensus fully adjusts

## Speculative Ideas

- He may use secondary sources much earlier than primary-source purists would prefer, then validate as conviction rises.
- He may choose source classes based on where the bottleneck lives:
  - pricing databases and feedstock trackers for materials
  - earnings/guidance and partner disclosures for cycle expressions
- `AXTI` and `SNDK` may represent two different sub-engines that the product should model separately rather than collapsing into one universal pipeline.

## Open Questions

1. Do we want to expand this archaeology into more names like `AAOI`, `LITE`, and `IQE` to see whether they cluster with the `AXTI` method or form a third pattern?
2. Do we want to classify all named sources in the archive into:
   - primary
   - secondary
   - market-pricing
   - social / specialist
3. Do we want to convert these findings into explicit product workflows:
   - `bottleneck discovery`
   - `cycle expression selection`
