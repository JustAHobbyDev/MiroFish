# True Blind Run Protocol v1

Date: March 20, 2026

## Purpose

Define the first honest experimental protocol for upstream discovery.

This protocol exists because retrospective case analysis is not enough.

We need a process that starts from:

- a broader mixed public corpus
- with no known narrowing target
- and no allowed use of case-specific hindsight during clustering

The protocol is designed to test:

- whether the system can surface enough signal to justify narrowing

It is not designed to test:

- final expression ranking
- bottleneck verification quality
- trade performance

## Core Principle

The blind run must be frozen before outcome evaluation.

This means:

1. clustering rules are fixed in advance
2. source universe is fixed in advance
3. time window is fixed in advance
4. run outputs are recorded before benchmark comparison

Only after those steps are complete may the outputs be compared to known
historical cases.

## Facts

1. The current photonics, memory, and control cases are useful for calibration,
   but they still embed hindsight at the case-selection level.

2. A real live run would begin with zero knowledge from any level of narrowing.

3. Therefore, the next honest step is not stronger retrospective rules.

4. The next honest step is a frozen blind run over a broader mixed corpus.

## Assumptions

1. The first true blind run can still be historical.

2. The corpus should be mixed enough that multiple possible pressure zones
   coexist.

3. The clustering pass should not know which benchmark case is expected to be
   present.

4. The same person may perform both the run and the evaluation, but only if the
   run outputs are frozen before evaluation begins.

## Non-Goals

This protocol does not attempt to solve:

1. production automation
2. live alerting
3. fully general source ingestion
4. benchmark selection fairness across all domains

It is a research protocol for honest evaluation.

## Corpus Requirements

The first blind run must use a broader mixed corpus, not only AleaBito's
archive.

### Required properties

1. multiple source classes
2. multiple possible systems/themes
3. time-bounded public information only
4. no target-specific curation

### Recommended source classes

1. company filings
2. earnings releases and transcripts
3. company press releases
4. trade press
5. policy or government notices where relevant
6. high-signal investor posts

These sources may contain indirect capital-flow evidence.

The extraction pass should not require explicit capital-allocation language if
the artifact plausibly implies procurement pull, buildout, or capacity response.

### Minimum corpus rule

The corpus must be broad enough that at least:

1. one true historical benchmark case is present
2. one plausible non-promoting/control pattern is present
3. multiple unrelated themes are also present

Otherwise the run is too easy.

## Time Window Rules

Each blind run must pre-register:

1. `corpus_start_date`
2. `corpus_end_date`
3. `time_bucket_rule`

Recommended default:

- `weekly`

Reason:

- daily is too noisy
- monthly is too coarse

## Frozen Inputs

Before the run begins, the following must be written down and not changed:

1. allowed source classes
2. corpus time window
3. signal extraction rules
4. signal type set
5. clustering features
6. promotion target format
7. output artifacts

If these change mid-run, the run is invalid.

## Forbidden Hindsight Inputs

During the blind run, the operator may not use:

1. final ticker names as search or clustering seeds
2. later bottleneck labels
3. later viral social-media summaries
4. post-cutoff evidence
5. manual cluster naming around a known answer
6. benchmark documents while clustering
7. prior artifact or cluster context during first-pass extraction

This applies even if the operator already personally knows the case.

## Allowed Clustering Features

The blind run may cluster only on upstream-neutral features.

### Allowed

1. demand drivers
2. system hints
3. architecture-shift language
4. stress language
5. visible-beneficiary recurrence
6. repeated entity adjacency
7. source-class diversity
8. time persistence

### Not allowed

1. target ticker as a seed
2. target bottleneck layer as a seed
3. target thesis label as a seed
4. manually inserted case-specific source packs

## Output Artifacts

Every blind run must produce these frozen outputs before evaluation:

### 1. Signal set

- all surfaced `capital_flow_signal_candidate`s

### 2. Cluster set

- all surfaced cluster candidates

### 3. Structural-pressure candidate set

- all surfaced `structural_pressure_candidate`s

### 4. Run log

- corpus definition
- extraction rules used
- clustering rules used
- timestamp of run completion

### 5. Narrowing decisions

For each structural-pressure candidate:

1. `enough_to_narrow`
2. `not_enough_to_narrow`

## Output Freeze Rule

Once the outputs above are written:

1. no new clustering logic may be added
2. no new sources may be added
3. no candidate may be renamed using benchmark hindsight
4. no new signal extraction rule may be introduced

Only after that freeze may evaluation begin.

## Evaluation Phase

After the run is frozen, compare outputs against benchmark cases.

### Evaluation questions

1. Did the run surface a structural-pressure candidate that corresponds to the
   historical case?
2. Did it do so early enough to justify narrowing?
3. Did it avoid promoting the control case?

### Success target

The primary success condition is:

- correct narrowing justification

Not:

- perfect ticker selection
- full bottleneck proof

## Operator / Evaluator Separation

This does not require two different people.

It does require two different phases.

### Phase A: run operator mode

- define corpus
- extract `capital_flow_signal_candidate`s artifact by artifact with the fixed
  zero-context prompt
- cluster signals
- freeze outputs

### Phase B: evaluator mode

- open benchmark notes
- compare frozen outputs to known cases
- score success/failure

The same person may do both phases only if:

1. the outputs are frozen first
2. the evaluation notes are created afterward

This is the minimum separation needed to reduce contamination.

## Recommended First Blind Run

### Corpus design

Use a mixed historical corpus that includes the relevant time windows for:

1. photonics / AI networking
2. memory / HBM / NAND
3. at least one control branch

The corpus should not be hand-trimmed to only benchmark-relevant items.

### Target benchmark visibility

The run should be capable of containing:

1. `Photonics -> AXTI`
2. `Memory -> SNDK`
3. `POET` control

But the clustering phase should not be told those are the targets.

## Success Conditions

A run is useful if all are true:

1. at least one benchmark pressure zone is surfaced
2. at least one control case correctly fails promotion
3. the surfaced candidates are explainable through frozen outputs
4. the run can be audited after the fact

## Failure Modes

1. `Corpus leakage`
   - source selection already bakes in the target

2. `Feature leakage`
   - clustering features implicitly encode the answer

3. `Evaluation leakage`
   - benchmark knowledge changes clustering before the run is frozen

4. `Trivial corpus`
   - the corpus is so narrow that the answer is the only thing that can emerge

5. `Overpromotion`
   - many vague candidates promote because the corpus is mixed and noisy

## Implementation Guidance

### Build first

1. mixed-corpus manifest format
2. frozen signal extraction config
3. frozen clustering config
4. run-log artifact
5. post-run evaluation sheet

### Do not build first

1. production thresholds
2. ranking logic
3. expression scoring

Those remain downstream of the blind-run evidence.

## Open Questions

1. What exact mixed corpus should be used for the first run:
   - one quarter
   - one six-month window
   - another historical slice

2. Should the first run be limited to text sources already locally archived, or
   should it include a fresh broad public reconstruction pass?

3. What is the minimum corpus breadth needed before the run is hard enough to be
   informative?
