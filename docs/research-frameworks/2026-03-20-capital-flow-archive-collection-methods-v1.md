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

The concrete rule set is defined in:

- [2026-03-20-capital-flow-event-form-prefilter-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-capital-flow-event-form-prefilter-v1.md)

## Source-Class Methods

## 1. Trade Press

### Why it is first-pass eligible

Broad industrial and technical trade press surfaces:

1. facility construction
2. equipment orders
3. deployment waves
4. manufacturing constraints
5. procurement shifts
6. capacity announcements
7. cross-company demand and bottleneck context

This is currently the strongest source class tested for early structural-pressure
discovery.

### Concrete sources

1. `Manufacturing Dive`
2. `Utility Dive`
3. `Data Center Dynamics`
4. `Semiconductor Engineering`
5. `EE Times`
6. `IndustryWeek`
7. `Supply Chain Dive`
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

### Current operating note

1. `trade_press` is the primary early-discovery lane
2. the current deterministic prefilter has been adjusted specifically for
   trade-press investment, factory, pipeline, and load-growth language
3. future scaling should start here before broadening government work further

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

### Current operating note

1. `company_release` is now best treated as a confirmation and corroboration
   lane
2. it is cleaner than broad government feeds, but more issuer-local than
   `trade_press`

## 3. Government

### Why it is first-pass eligible

Government sources can still surface:

1. direct project authorizations
2. land and resource access changes
3. project-linked awards and spending
4. narrow implementation signals

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
2. publisher
3. publication date
4. title
5. body text
6. source tags or categories

### Current operating note

1. broad government feeds are secondary, not primary
2. use them narrowly for:
   - construction / project authorization
   - land and resource access changes
   - implementation-stage corroboration
3. do not spend more time broadening government edge-case handling until the
   larger `trade_press` lane is more mature
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
2. run deterministic event-form prefilter
3. preserve `drop` decisions for audit until rejection quality is validated
4. run zero-context extraction to produce `capital_flow_signal_candidate`s on
   surviving artifacts
5. cluster those candidates into possible structural-pressure zones
6. only then deepen into issuer-specific filing collection

## Validation Requirement

The first deterministic prefilter is not considered trusted by default.

It must be validated empirically by reviewing rejected artifacts after early
runs.

Minimum validation loop:

1. log all dropped artifacts
2. review a sample after each run
3. identify false negatives
4. relax or revise rules if false negatives are too frequent

Until this audit loop is completed repeatedly, the prefilter should be treated
as a cost-control mechanism under test, not as a proven discovery gate.

## Open Questions

1. Should the event-form prefilter be represented as:
   - a fixed lexical list
   - a small rule set with regex families
   - or a tiny classifier

2. Should the first archive preserve full raw HTML for all source classes, or
   normalized text plus metadata only?
