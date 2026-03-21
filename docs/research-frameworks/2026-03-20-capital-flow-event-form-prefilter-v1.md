# Capital-Flow Event-Form Prefilter v1

Date: March 20, 2026

## Purpose

Define the first pre-LLM filter for archive collection.

This prefilter exists to reduce collection volume without reintroducing:

1. ticker hindsight
2. industry hindsight
3. benchmark-company selection

It should answer only:

- does this artifact look like an event that may imply directional capital
  flow, procurement pull, capacity response, or physical buildout?

It should not answer:

- is this artifact relevant to a known thesis?
- is this the right company?
- is this the right bottleneck?

## Facts

1. The first-pass archive is venue-level and broad.

2. Some sources are too high-volume to collect naively without any filtering.

3. Capital-flow evidence is often indirect.

4. Therefore the prefilter must look for event forms, not theme conclusions.

5. Event-form filtering is less contaminating than:
   - ticker filters
   - issuer filters
   - industry filters
   - benchmark-theme filters

## Assumptions

1. The first prefilter should be simple and auditable.

2. False positives are acceptable.

3. False negatives are more dangerous than moderate over-collection at this
   stage.

4. The prefilter should be deterministic before any LLM interpretation begins.

5. The first deployed version of the prefilter should be treated as
   provisional until its rejected artifacts have been audited after real runs.

## Non-Goals

This prefilter is not trying to do:

1. semantic thesis detection
2. bottleneck detection
3. company ranking
4. clustering
5. document summarization

## Recommended Representation

Use a hybrid rule set:

1. event-form lexical families
2. regex families for common phrase variants
3. source-field weighting
4. triage output

Do not use:

1. issuer allowlists
2. ticker allowlists
3. industry-specific keyword packs
4. historical benchmark company names

## Why this representation

### Facts

1. Pure lexical matching is easy to audit but brittle.
2. A tiny classifier would be harder to inspect at this stage.
3. Regex families are enough to capture common event variants.

### Recommendation

Use:

- lexical families + regex families first

Defer:

- classifier-based prefiltering

## Allowed Input Fields

The prefilter may inspect only:

1. title
2. headline
3. subheadline or deck
4. section name
5. category tags
6. publisher-provided metadata

It may not inspect:

1. full body text
2. prior artifacts
3. prior clusters
4. benchmark notes

Reason:

- the prefilter should remain shallow and cheap
- deeper interpretation belongs to the LLM extraction pass

## Triage Output

Each artifact gets one of:

1. `keep`
2. `review`
3. `drop`

### `keep`

Use when:

- event-form evidence is strong and explicit in allowed fields

### `review`

Use when:

- event-form evidence is plausible but ambiguous
- multiple weak indicators appear together

### `drop`

Use when:

- no event-form evidence appears

Important:

- `drop` is still a provisional judgment in v1
- dropped artifacts must be logged for later audit until rejection quality is
  validated empirically

## Event-Form Families v1

The first rule set should be broad and capital-flow-shaped.

## 1. Awards and Funding

Examples:

1. award
2. grant
3. loan
4. subsidy
5. funding
6. financing
7. incentive
8. tax credit
9. loan guarantee

Example regex ideas:

1. `\\baward(?:ed|s)?\\b`
2. `\\bgrant(?:ed|s)?\\b`
3. `\\bloan(?:s|ed)?\\b`
4. `\\bsubsid(?:y|ies|ized|ising)\\b`

## 2. Contracts and Orders

Examples:

1. contract
2. order
3. booked
4. booking
5. purchase order
6. procurement
7. supply agreement
8. offtake
9. framework agreement

Example regex ideas:

1. `\\bcontract(?:s|ed| award)?\\b`
2. `\\border(?:s|ed| book| booking)?\\b`
3. `\\bprocurement\\b`
4. `\\bsupply agreement\\b`
5. `\\bofftake\\b`

## 3. Facility and Capacity Expansion

Examples:

1. expand
2. expansion
3. capacity
4. capacity increase
5. new facility
6. new plant
7. new fab
8. new line
9. ramp
10. scale-up
11. manufacturing buildout

Example regex ideas:

1. `\\bexpand(?:ing|ed|s|ion)?\\b`
2. `\\bcapacity(?: increase| expansion| additions?)?\\b`
3. `\\bnew (?:facility|plant|fab|line)\\b`
4. `\\bramp(?:ing|ed|s)?\\b`

## 4. Construction and Deployment

Examples:

1. groundbreaking
2. construction
3. buildout
4. deployment
5. rollout
6. commissioning
7. opening
8. operational
9. start of operations

Example regex ideas:

1. `\\bgroundbreak(?:ing)?\\b`
2. `\\bconstruction\\b`
3. `\\bbuildout\\b`
4. `\\bdeploy(?:ment|ed|ing|s)?\\b`
5. `\\brollout\\b`
6. `\\bstart of operations\\b`

## 5. Partnerships with Buildout Implications

Examples:

1. partnership
2. collaboration
3. joint venture
4. strategic agreement
5. manufacturing agreement
6. supply partnership

Important note:

- partnership language alone is weak
- this family should rarely trigger `keep` by itself
- it is mainly useful as a `review` signal when combined with stronger forms

## Source-Field Weighting

Use a simple field hierarchy.

### Strong fields

1. title
2. headline
3. subheadline

### Medium fields

1. section name
2. category tags

### Weak fields

1. miscellaneous metadata labels

## Triage Rules v1

### `keep`

Return `keep` when either is true:

1. at least one strong-field hit from:
   - awards and funding
   - contracts and orders
   - facility and capacity expansion
   - construction and deployment
2. two or more distinct family hits across allowed fields

### `review`

Return `review` when either is true:

1. exactly one weak or ambiguous hit exists
2. only partnership/collaboration language appears
3. one medium-field hit exists without a strong-field hit

### `drop`

Return `drop` when:

1. no family hit exists
2. the only matches are generic business language with no buildout form

## Explicitly Excluded Patterns

Do not treat these as sufficient by themselves:

1. `AI`
2. `growth`
3. `innovation`
4. `market opportunity`
5. `strategic`
6. `leadership`
7. `next generation`
8. `strong demand`

Reason:

- these are too narrative-heavy without event form

## Source-Class Application

## Government

Use:

1. keep almost everything from narrowly scoped sources
2. use the prefilter mainly for very broad feeds or award databases

Additional note for broad government feeds:

1. planning-enablement notices should default to `review`, not `keep`
2. examples:
   - `record of decision`
   - `integrated activity plan`
   - `public land order`
   - `lease sale`
3. reason:
   - these can precede capital deployment
   - but they are usually one step upstream of direct buildout evidence

## Company Release

Use the prefilter aggressively on:

1. title
2. subheadline
3. release category

This is likely the highest-volume first-pass class.

This is also the first class where rejection audits should be run, because it
is likely to expose over-aggressive filtering fastest.

## Trade Press

Use the prefilter on:

1. headline
2. deck
3. section
4. tags

This class should allow more `review` outcomes than company releases.

## Example Outcomes

### `keep`

Headline:

- `Company X breaks ground on new battery materials plant`

Reason:

1. `groundbreak`
2. `new plant`
3. explicit construction/buildout form

### `review`

Headline:

- `Company Y and Company Z announce strategic partnership for next-generation networking`

Reason:

1. partnership language exists
2. no explicit spend, order, expansion, or deployment form

### `drop`

Headline:

- `Company Q launches new branding initiative`

Reason:

1. no capital-flow event form

## Implementation Guidance

### Build first

1. canonical event-form family list
2. regex family list
3. triage function returning:
   - `keep`
   - `review`
   - `drop`
4. provenance fields showing which rules fired
5. rejected-artifact logging for post-run audit

### Build later

1. statistical tuning
2. classifier fallback
3. source-specific threshold tuning

## Validation Rule

The deterministic prefilter must not be trusted on theory alone.

For early runs:

1. store all `drop` decisions with:
   - artifact id
   - source class
   - title/headline
   - fired rules
   - timestamp
2. sample and review dropped artifacts after each run
3. classify reviewed drops as:
   - correct_drop
   - borderline_should_review
   - false_negative
4. revise the prefilter only after reviewing those logged drops

The prefilter graduates from provisional to trusted only after repeated audits
show that rejection quality is acceptable.

## Open Questions

1. Should `review` artifacts be collected in the first run, or only logged for
   later inspection?

2. Should source-class-specific thresholds differ in v1, or stay uniform for
   auditability?
