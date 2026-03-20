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
3. `earnings_transcript`
4. `government`
5. `trade_press`
6. `investor_post`

Keep it there for v1.

Do not add more classes until the first run is complete.

## Source Universe For First Archive

The first archive should not be built around target tickers or target domains.

It should be built around concrete sources and venues.

Collection must happen by source-level inclusion rules, not by theme-level
filtering.

### Company filings

Concrete sources:

- `AXT` filings via `SEC EDGAR`
- `Micron` filings via `SEC EDGAR`
- `Lumentum` filings via `SEC EDGAR`
- `Coherent` filings via `SEC EDGAR`
- `Sandisk` filings via `SEC EDGAR`

### Company releases

Concrete sources:

- `NVIDIA Investor Relations`
- `Broadcom Investor Relations`
- `Micron Investor Relations`
- `SK hynix Newsroom`
- `Samsung Newsroom`
- `Sandisk Newsroom`
- `Lumentum Investor Relations`
- `Coherent Newsroom`
- `JX Advanced Metals News Releases`

### Earnings transcripts

Concrete sources:

- `Micron`
- `SK hynix`
- `Sandisk`

### Government

Concrete sources:

- `BIS`
- `Federal Register`
- `SEC EDGAR`

### Trade press

Concrete sources:

- `SemiAnalysis`
- `TrendForce`
- `DigiTimes`
- `LightCounting`

### Investor posts

Concrete sources:

- `@aleabitoreddit`

Rule:

- investor posts are one layer of the archive, not the archive itself
- a source may be concrete even if the class remains small in v1
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
    earnings_transcript/
    government/
    trade_press/
    investor_post/
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
- generated `signal_candidate`s

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

## Collection Policy

The archive must be collected by source-level inclusion, not by theme-level
filtering.

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

1. captures photonics buildup
2. captures memory buildup
3. captures control-like side branches
4. includes enough unrelated material to make the blind run harder

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

2. Should we cap investor-post accounts for the first run, or keep the class
   broad and let the manifest enumerate accounts explicitly?

3. Do we want the first normalized layer to stop at `source` objects, or also
   include first-pass `signal_candidate` generation?
