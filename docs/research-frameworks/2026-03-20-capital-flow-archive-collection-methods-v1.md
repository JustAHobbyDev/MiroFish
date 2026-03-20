# Capital-Flow Archive Collection Methods v1

Date: March 20, 2026

## Purpose

Define how each source class in the first archive is collected without
introducing company, industry, or benchmark hindsight.

This spec answers:

1. what an artifact is for each source class
2. what gets collected at first pass
3. what pre-LLM filtering is allowed
4. what is deferred until after narrowing

## Facts

1. The first pass must start from broad evidence of possible directional capital
   movement.

2. The first pass should not assume:
   - the right company
   - the right industry
   - the right bottleneck

3. Some source universes are practical for first-pass broad collection:
   - government notices
   - wire releases
   - broad trade press

4. Some source universes are too broad or too company-specific for honest
   first-pass collection:
   - issuer-level EDGAR harvesting

5. Therefore first-pass discovery collection and second-pass enrichment
   collection must be separated.

## Assumptions

1. The first archive should be broad but not infinite.

2. The only acceptable pre-LLM filtering at collection time is event-form
   filtering tied to possible capital-flow implications.

3. Event-form filtering is less biased than company, ticker, or theme-based
   filtering.

## Non-Goals

This spec does not define:

1. the LLM extraction prompt
2. clustering logic
3. promotion thresholds
4. post-narrowing verification workflows

## Core Collection Principle

Use venue-level collection plus event-form filtering.

Do not use:

1. ticker filters
2. benchmark-company filters
3. target-industry filters
4. known-bottleneck labels

## Allowed Event-Form Prefilter

This prefilter is allowed only on:

1. title
2. headline
3. subheadline or deck
4. section metadata
5. official category tags, if available

It should never inspect a document and decide relevance using the known case
answer.

### Event-form concepts

The prefilter may keep artifacts that appear to involve:

1. awards
2. grants
3. loans
4. subsidies
5. contracts
6. procurement
7. orders
8. supply agreements
9. facility openings
10. plant, fab, or line expansions
11. manufacturing buildout
12. capacity additions
13. deployment rollouts
14. construction starts or groundbreakings

These are collection-shaping hints, not final signal labels.

## Source-Class Methods

## 1. Government

### Why it is first-pass eligible

Government sources directly surface:

1. public spending
2. industrial-policy support
3. contract awards
4. subsidy-backed buildout
5. infrastructure deployment

### Concrete sources

1. `BIS`
2. `Federal Register`
3. `DOE Loan Programs Office`
4. `Office of Clean Energy Demonstrations`
5. `CHIPS Program Office`
6. `DoD Contract Announcements`
7. `USASpending Award Data`

### Artifact boundary

One artifact equals:

1. one notice
2. one award record
3. one release
4. one announcement page

### Collection rule

Collect all in-window artifacts from these sources.

If the source is too broad for direct full capture, apply only the allowed
event-form prefilter to title or metadata.

### Preserve

1. source URL
2. publication date
3. publisher
4. title
5. body text
6. source tags or categories

## 2. Company Release

### Why it is first-pass eligible

Wire services surface:

1. expansions
2. new facilities
3. orders
4. supply agreements
5. partnerships tied to buildout
6. deployment announcements

These often appear before deeper company-specific research begins.

### Concrete sources

1. `Business Wire`
2. `PR Newswire`
3. `GlobeNewswire`

### Artifact boundary

One artifact equals one release page.

### Collection rule

Collect all in-window release artifacts that pass the allowed event-form
prefilter on:

1. headline
2. subheadline
3. release category metadata when available

Do not filter by:

1. issuer
2. ticker
3. benchmark company
4. benchmark industry

### Preserve

1. release URL
2. publisher
3. issuing company name
4. publication date
5. headline
6. body text
7. category metadata

## 3. Trade Press

### Why it is first-pass eligible

Broad industrial and technical trade press surfaces:

1. facility construction
2. equipment orders
3. deployment waves
4. manufacturing constraints
5. procurement shifts
6. capacity announcements

without needing a benchmark-seeded company universe.

### Concrete sources

1. `IndustryWeek`
2. `Manufacturing Dive`
3. `Supply Chain Dive`
4. `Utility Dive`
5. `Data Center Dynamics`
6. `Semiconductor Engineering`
7. `EE Times`
8. `Fierce Electronics`

### Artifact boundary

One artifact equals one article page.

### Collection rule

Collect all in-window articles that pass the allowed event-form prefilter on:

1. headline
2. deck
3. section name
4. article tags when available

Do not filter by:

1. target company
2. target component
3. target bottleneck
4. known benchmark theme

### Preserve

1. article URL
2. publisher
3. published date
4. headline
5. deck if available
6. body text
7. section/tag metadata

## 4. Company Filing

### Why it is not first-pass eligible

Raw EDGAR is too broad and too issuer-dependent for honest first-pass
collection.

Using it at stage one would force one of two bad choices:

1. collect an impractically huge corpus
2. pre-select issuers in a way that leaks narrowing

### Role

`company_filing` is a deferred enrichment source class.

It is used only after:

1. a structural-pressure candidate forms
2. narrowing identifies candidate issuers or systems worth deepening

### Deferred sources

1. `SEC EDGAR 8-K`
2. `SEC EDGAR 10-Q`
3. `SEC EDGAR 10-K`
4. `SEC EDGAR 20-F`

### Deferred collection rule

After narrowing, collect filings only for issuers surfaced by the narrowed
research universe and only within the pre-registered time boundary.

### Artifact boundary

One artifact equals one filing document plus section-level segmentation.

## Collection Order

Use this order for the first archive:

1. `government`
2. `company_release`
3. `trade_press`

Use this order only after narrowing:

1. `company_filing`

## Resulting Workflow

1. collect broad first-pass artifacts from capital-flow-first venues
2. run zero-context extraction to produce `capital_flow_signal_candidate`s
3. cluster those candidates into possible structural-pressure zones
4. only then deepen into issuer-specific filing collection

## Open Questions

1. Should the event-form prefilter be represented as:
   - a fixed lexical list
   - a small rule set with regex families
   - or a tiny classifier

2. Should the first archive preserve full raw HTML for all source classes, or
   normalized text plus metadata only?
