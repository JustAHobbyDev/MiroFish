# AleaBito Blind Discovery Capability Assessment v1

Date: March 22, 2026

## Purpose

Assess whether the current system appears capable of rediscovering
`AleaBito`-style expressions blindly, using only:

1. approximate historical time windows
2. public information available before the move

The question is not:

1. can we restate his final picks after the rerating
2. can we exactly match his ticker order

The question is:

1. can we recover enough blind signal to justify narrowing into the right
   research universe early enough to matter?

## Facts

### Existing worked benchmark cases

The repo currently contains three relevant historical calibration cases.

1. Positive case:
   - `Photonics -> AXTI`
   - [2026-03-20-photonics-axti-historical-signal-calibration-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-20-photonics-axti-historical-signal-calibration-v1.md)

2. Positive case:
   - `Memory -> SNDK`
   - [2026-03-20-memory-sndk-historical-signal-calibration-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-20-memory-sndk-historical-signal-calibration-v1.md)

3. Control case:
   - `POET standalone workaround branch`
   - [2026-03-20-poet-control-historical-signal-calibration-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-20-poet-control-historical-signal-calibration-v1.md)

### What those cases currently show

`AXTI`

1. Blind result:
   - `blind_pass`
2. Blind narrowing justified:
   - `true`
3. Blind role coverage:
   - `5 / 6`
4. Blind recall ratio:
   - `0.53`
5. Blind surfaced enough signal to justify:
   - `AI photonics` universe narrowing
6. Blind surfaced:
   - visible beneficiaries first
   - upstream clue later
7. Blind did **not** yet prove the final `InP chokepoint` by itself

`SNDK`

1. Blind result:
   - `blind_pass`
2. Blind narrowing justified:
   - `true`
3. Blind role coverage:
   - `4.5 / 6`
4. Blind recall ratio:
   - `0.46`
5. Blind surfaced enough signal to justify:
   - `AI memory` universe narrowing
6. Blind did **not** strongly validate `SNDK` as the final preferred
   expression, but it did surface the memory cycle and include `SNDK` inside
   that universe

`POET`

1. Blind result:
   - `blind_fail`
2. Blind narrowing justified:
   - `false`
3. Blind role coverage:
   - `2 / 6`
4. This is a useful control because:
   - the name was real
   - the adjacency was real
   - but the system correctly judged that it should **not** form its own
     standalone structural-pressure candidate

### Aggregate pattern from current evidence

Across the current worked cases:

1. The system can recover enough blind signal to justify narrowing into the
   right broad universe in at least two nontrivial AleaBito-related cases.
2. The system can also reject an adjacent but weaker standalone branch in a
   control case.
3. The system is better at:
   - `universe formation`
   - `chain orientation`
   - `visible-beneficiary-first discovery`
4. The system is weaker at:
   - proving the final hidden bottleneck immediately
   - selecting the final best expression with high confidence from the blind
     pass alone

## Assessment

### What we can claim now

We can reasonably claim:

1. The system appears capable of blind **early-universe discovery** for some
   AleaBito-style cases.
2. It is not merely overfitting to positive cases, because the `POET` control
   stayed blocked.
3. The current product shape matches the repo's own working hypothesis:
   - detect pressure
   - form the right system
   - identify visible beneficiaries
   - walk upstream
   - verify bottlenecks later

### What we cannot claim yet

We cannot yet claim:

1. that the system can blindly reproduce AleaBito's **final expression picks**
   in general
2. that it can do so **early enough** across a broad set of cases
3. that it has a demonstrated timing edge beyond a few curated calibrations
4. that it can run a fully frozen mixed-corpus blind pass without case-level
   hindsight in corpus design

### Best current answer to the user question

If the question is:

- "Are we capable of discovering these expressions blind in all regards other
  than the approximate time window where we would have needed to find evidence
  for them?"

The best current answer is:

1. **Partially yes** for:
   - discovering the correct pressure universe
   - justifying narrowing
   - surfacing some candidate expressions inside that universe
2. **Not yet proven** for:
   - consistently identifying the final best expression
   - doing so early enough across a fair benchmark set
   - doing so from a fully frozen mixed corpus

## Why This Matters

This means the current system is already more than:

1. post-hoc narrative reconstruction

But it is still less than:

1. a proven early-discovery engine with a demonstrated market edge

That is meaningful progress.

It is not the end proof.

## Decision

The correct current posture is:

1. treat the system as **promising but unproven**
2. treat existing positive cases as:
   - evidence that the architecture is directionally right
3. do **not** treat current results as proof that the edge is already solved

## Highest-Leverage Next Proof Step

The next best experiment is not more single-name research.

It is:

1. a frozen historical blind run over a broader mixed corpus
2. with pre-registered source universe
3. with pre-registered cutoff dates
4. and with evaluation only after outputs are frozen

This is already described in:

- [2026-03-20-true-blind-run-protocol-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-true-blind-run-protocol-v1.md)

## Open Questions

1. How many positive and control cases are enough before we say the system is
   genuinely validated?
2. What minimum lead time counts as success?
   - `3 months`
   - `6 months`
   - `12 months`
3. Should success be defined as:
   - correct universe formation
   - correct final expression
   - or a staged version of both?
