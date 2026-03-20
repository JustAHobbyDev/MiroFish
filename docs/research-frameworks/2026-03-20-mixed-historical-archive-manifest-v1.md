# Mixed Historical Archive Manifest v1

Date: March 20, 2026

## Purpose

Define the archive contract for the first true blind run.

This is the layer between:

- source planning
- and actual corpus collection

The manifest must answer:

1. what time window is frozen
2. which source classes are in scope
3. which concrete source targets are in scope
4. where raw and normalized captures are stored
5. how the archive stays auditable

## Recommendation

Use a six-month archive window for the first blind run.

Reason:

1. one quarter is too narrow for signal buildup
2. six months is broad enough to contain:
   - photonics
   - memory
   - a control branch
   - unrelated themes
3. six months is still small enough to freeze and audit

## Facts

1. We already have source-class prioritization in:
   - [2026-03-16-source-priority-matrix-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-16-source-priority-matrix-v1.md)

2. We already have ingestion-shape guidance in:
   - [2026-03-16-source-ingestion-and-structural-parsing-schema-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-16-source-ingestion-and-structural-parsing-schema-v1.md)

3. We do not yet have a frozen mixed archive suitable for a true blind run.

4. A source list is not enough.
   - We need a captured corpus with provenance and freeze rules.

## Assumptions

1. The first archive should optimize for discovery experimentation, not
   production coverage.

2. The archive should be broad enough to avoid trivial answers.

3. The archive should preserve raw captures and normalized records separately.

## Non-Goals

This manifest is not trying to define:

1. every future source we may ever ingest
2. production alerting cadences
3. full live crawling infrastructure
4. the final database schema

## Required Manifest Fields

Every archive manifest must include:

### Identity

1. `archive_id`
2. `archive_version`
3. `created_at`
4. `owner`
5. `purpose`

### Time bounds

1. `corpus_start_date`
2. `corpus_end_date`
3. `time_bucket_rule`

### Scope

1. `source_classes`
2. `source_universe`
3. `collection_policy`
4. `exclusions`

### Storage

1. `raw_root`
2. `normalized_root`
3. `manifests_root`
4. `logs_root`

### Freeze rules

1. `frozen_inputs`
2. `frozen_outputs`
3. `forbidden_hindsight_inputs`

## Source Classes For First Archive

Use these classes for the first six-month archive:

1. `company_filing`
2. `company_release`
3. `government`
4. `trade_press`

Keep it there for v1.

Do not add more classes until the first run is complete.

## Source Universe For First Archive

The first archive should not be built around target tickers or target domains.

It should be built around concrete sources and venues.

Collection must happen by source-level inclusion rules, not by theme-level
filtering.

The first archive should be capital-flow-first.

That means:

1. source selection should favor venues where directional spending, buildout,
   procurement, awards, expansion, and capacity response appear
2. source selection should not depend on knowing which company or industry is
   undervalued
3. signals may be indirect and need LLM interpretation later
4. the source universe should therefore be venue-level and broad

### Company filings

Concrete sources:

- `SEC EDGAR 8-K`
- `SEC EDGAR 10-Q`
- `SEC EDGAR 10-K`
- `SEC EDGAR 20-F`

### Company releases

Concrete sources:

- `Business Wire`
- `PR Newswire`
- `GlobeNewswire`

### Government

Concrete sources:

- `BIS`
- `Federal Register`
- `DOE Loan Programs Office`
- `Office of Clean Energy Demonstrations`
- `CHIPS Program Office`
- `DoD Contract Announcements`
- `USASpending Award Data`

### Trade press

Concrete sources:

- `IndustryWeek`
- `Manufacturing Dive`
- `Supply Chain Dive`
- `Utility Dive`
- `Data Center Dynamics`
- `Semiconductor Engineering`
- `EE Times`
- `Fierce Electronics`

Rule:

- a source belongs in the first archive if it regularly surfaces capital-flow
  indicators before deep company-specific narrowing
- investor posts are excluded from the first blind run to avoid social
  synthesis dominating the first-stage corpus
- expanding the source universe requires a new manifest version

## Archive Layout

Recommended layout:

```text
research/archive/
  manifests/
  runs/
  raw/
    company_filing/
    company_release/
    government/
    trade_press/
  normalized/
    sources/
    signals/
  logs/
```

### Raw

Contains:

- original fetched content
- minimal source metadata
- no hindsight labels

### Normalized

Contains:

- canonical source objects
- normalized text/fragments
- generated `capital_flow_signal_candidate`s

### Runs

Contains:

- blind-run manifests
- frozen run outputs

### Logs

Contains:

- collection logs
- normalization logs
- provenance errors

## Collection Rules

1. preserve original source URL
2. preserve published date
3. preserve retrieved date
4. preserve source class
5. preserve publisher / author when available
6. preserve text hash after normalization
7. preserve artifact boundaries so first-pass interpretation can remain
   artifact-local

## Collection Policy

The archive must be collected by source-level inclusion, not by theme-level
filtering.

Interpretation may happen later with an LLM, but collection itself must remain
blind to benchmark cases and target industries.

Allowed collection rule:

- collect all in-window items from the listed concrete sources

Forbidden collection rules:

1. collect only photonics items
2. collect only memory items
3. collect only items mentioning known benchmark tickers
4. collect only items already believed to be relevant

Signal collection should shape later domain research.
Domain shaping should not shape initial archive collection.

## Freeze Rules

Once the manifest is approved for a run:

1. no source class changes
2. no source target changes
3. no time-window changes
4. no hindsight additions to the archive

Changes require:

- a new manifest version

## Exclusions

The first archive should exclude:

1. post-cutoff benchmark materials
2. manually written benchmark summaries
3. current-day retrospective memos
4. derived evaluation notes

Those belong in evaluation, not in the archive.

## First Archive Recommendation

Use:

- `corpus_start_date`: `2025-09-01`
- `corpus_end_date`: `2026-02-28`
- `time_bucket_rule`: `weekly`

Reason:

1. captures multiple capital-flow waves across the same broad market period
2. is long enough for indirect signals to accumulate before narrowing
3. includes enough unrelated material to make the blind run harder
4. does not require pre-selecting benchmark industries during collection

## Implementation Guidance

### Build now

1. archive directory layout
2. first manifest file
3. collection log format
4. normalized source record format

### Build later

1. automated refreshes
2. broader source classes
3. live collection cadence

## Open Questions

1. Should the first archive include only English-language sources?

2. Do we want the first normalized layer to stop at `source` objects, or also
   include first-pass `capital_flow_signal_candidate` generation?
