# Signal Candidate v1

Date: March 20, 2026

## Purpose

Define the first atomic discovery object in the upstream workflow.

A `signal_candidate` is:

- weaker than a thesis
- weaker than a bounded universe
- weaker than a structural pressure candidate

It is the smallest normalized public observation that the system can reuse,
cluster, and promote.

This spec is deliberately narrow.

It covers:

- signals relevant to rising-demand structural pressure

It does not yet cover:

- constrained-access archetypes
- legal exclusivity
- reimbursement gating
- full polarity or sentiment modeling

## Why This Object Exists

The system needs a unit smaller than `structural_pressure_candidate`.

Reason:

- a structural pressure candidate should never be formed from one article,
  filing, or investor post
- but the system still needs to preserve individual observations in a reusable
  way

So the workflow should begin with:

1. raw public information
2. `signal_candidate`
3. `structural_pressure_candidate`
4. bounded universe

## Facts

1. A single public observation can be meaningful, but it is not enough to
   justify deep narrowing.

2. The first useful unit needs:
   - provenance
   - time boundary
   - concrete statement
   - preliminary system relevance

3. If the unit is too large, it becomes a mini-thesis.

4. If the unit is too small, it becomes raw text with no reusable structure.

## Assumptions

1. Most useful early discoveries emerge from multiple weak-to-medium public
   observations aligning.

2. The first v1 implementation should optimize for industrial demand pressure,
   not broad universal news understanding.

3. `signal_candidate` should be atomic enough to cluster, but rich enough to
   preserve why it might matter.

## Non-Goals

This object is not trying to answer:

1. whether the thesis is true
2. whether the system is definitely bottlenecked
3. which company is the best expression
4. whether the market is mispricing the situation
5. what the final bounded universe should be

Those are downstream.

## Definition

A `signal_candidate` is a normalized public observation that may indicate:

- rising demand
- buildout acceleration
- supply-chain stress
- manufacturing response
- architecture change

but is not yet strong enough on its own to justify a research universe.

It is stronger than:

- raw source text
- an isolated headline
- an unstructured ticker mention

It is weaker than:

- a structural pressure candidate

## Required Invariants

Every valid `signal_candidate` must have all of these:

1. `Source provenance`
   - exact source reference
   - source class
   - time boundary

2. `Observable statement`
   - one concrete fact, event, claim, or observation
   - not a broad narrative summary

3. `Primary signal type`
   - exactly one dominant type for v1

4. `Preliminary implication`
   - a plain-language reason this may matter physically or economically

5. `System hint`
   - a provisional hint about the affected system, component family, company set,
     or industrial area

If any invariant fails, the object should not exist.

## Design Rules

### Atomicity

A `signal_candidate` should contain:

- one observation
- one dominant interpretation

If a source contains three materially different observations, split them into
three signals.

### Scope discipline

Do not let the object turn into:

- a chain map
- a bottleneck claim
- a candidate-expression memo

That is premature.

## Supported Signal Types v1

Keep the first type set narrow.

### `demand_acceleration`

Use when:

- spend, orders, adoption, capex, deployment, or demand are clearly increasing

Examples:

- TPU ramp
- higher optical demand
- infrastructure spend rising

### `capacity_tightness`

Use when:

- a source indicates supply is sold out, constrained, or unable to ramp easily

Examples:

- lead times rising
- production sold out
- shortage language

### `manufacturing_expansion`

Use when:

- a company or supplier adds facilities, lines, tooling, or capacity in response
  to demand

Examples:

- fab expansion
- packaging facility
- optical manufacturing line expansion

### `customer_pull`

Use when:

- a major customer, qualification, or order pull makes demand more concrete

Examples:

- hyperscaler qualification
- direct customer ramp
- major supply agreement

### `architecture_shift`

Use when:

- a new design or deployment model changes the intensity of component or
  material demand

Examples:

- CPO adoption
- higher optical intensity
- a system design that increases advanced packaging demand

### `policy_or_regulatory_support`

Use only when:

- the policy directly increases buildout, adoption, or demand

Examples:

- subsidy driving deployment
- direct policy support for infrastructure buildout

## Minimal Shape

This is not final storage schema.
It is the minimum working contract.

```json
{
  "signal_id": "sig_photonics_2025_12_01_001",
  "as_of_date": "2025-12-01",
  "status": "candidate",
  "source_class": "investor_post",
  "source_ref": {
    "platform": "x",
    "author": "aleabitoreddit",
    "post_id": "1234567890"
  },
  "signal_type": "demand_acceleration",
  "statement": "LITE is directly correlated to TPU ramp up.",
  "entities": [
    "LITE",
    "TPU"
  ],
  "system_hints": [
    "AI photonics",
    "TPU networking"
  ],
  "preliminary_implication": "Rising TPU deployment may increase demand for optical networking layers.",
  "confidence": "low"
}
```

## Required Fields

### Identity

1. `signal_id`
2. `as_of_date`
3. `status`

### Source

1. `source_class`
2. `source_ref`

### Observation

1. `signal_type`
2. `statement`
3. `entities`

### Interpretation

1. `system_hints`
2. `preliminary_implication`
3. `confidence`

## Source Rules

### Allowed input classes

1. company filings
2. earnings releases
3. earnings transcripts
4. company press releases
5. trade press
6. policy or government notices
7. high-signal investor posts

### Weak-source rule

Investor posts and trade summaries are allowed to create signals.

They are not allowed to prove a bottleneck by themselves.

### Statement rule

The `statement` field should preserve the actual observation in plain language.

It should not rewrite the source into a larger thesis.

## Confidence Bands

These bands describe observation quality, not thesis quality.

### `low`

- the observation is plausible
- source is weak or indirect
- interpretation is still provisional

### `medium`

- the observation is concrete
- system relevance is clear
- source is credible enough to keep and cluster

### `high`

- the observation is direct
- source is strong
- the implication is still preliminary, but the underlying observation is solid

High confidence does not mean the bottleneck thesis is true.

## Promotion Rules

### Raw public information -> signal candidate

Promote when all are true:

1. one concrete observation can be stated plainly
2. the source is traceable
3. the observation suggests possible system relevance

### Signal candidate -> reject

Reject when any are true:

1. the observation is too vague to state cleanly
2. the source cannot be traced
3. the statement is just generic thematic chatter
4. the observation is actually multiple signals bundled together

### Signal candidate -> structural pressure candidate

A single signal should not promote alone.

Promotion requires:

1. multiple compatible signal candidates
2. repeated evidence of rising demand or buildout
3. enough system grounding to name a real physical system
4. a plausible stress rationale

This promotion is defined in:

- [2026-03-20-structural-pressure-candidate-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-structural-pressure-candidate-v1.md)

## Examples

### Example 1: demand acceleration

Observation:

- `LITE is directly correlated to TPU ramp up`

Valid signal:

- `signal_type`: `demand_acceleration`
- `system_hints`: `AI photonics`, `TPU networking`

Why valid:

- concrete observation
- traceable source
- clear possible system implication

### Example 2: manufacturing expansion

Observation:

- company announces a new InP-related manufacturing expansion

Valid signal:

- `signal_type`: `manufacturing_expansion`
- implication: demand is strong enough to justify added capacity

### Example 3: invalid signal

Observation:

- `AI is a huge opportunity and many stocks will benefit`

Why invalid:

1. not concrete
2. no single observable statement
3. no real system hint
4. no traceable implication beyond theme enthusiasm

## Workflow Position

The intended order is:

1. raw public information
2. `signal_candidate`
3. `structural_pressure_candidate`
4. bounded universe formation
5. visible beneficiary identification
6. chain expansion
7. bottleneck candidate
8. verification
9. expression selection

## Failure Modes

1. `Signal inflation`
   - too many vague statements become signals

2. `Mini-thesis creep`
   - one signal contains too much derived reasoning

3. `Source blindness`
   - source is not preserved, so the signal cannot be audited later

4. `Premature promotion`
   - a single strong-seeming signal becomes a structural pressure candidate
     without enough corroboration

## Implementation Guidance

### Build first

1. source-normalized observation extraction
2. narrow signal-type classification
3. system-hint capture
4. lightweight confidence assignment

### Do not build first

1. rich scoring models
2. chain-role assignment
3. expression ranking logic
4. generalized non-demand bottleneck archetypes

## Open Questions

1. Should `system_hints` stay free text in v1, or move to controlled labels
   early?

2. Should `entities` be required to include at least one company, component, or
   system term?

3. What is the minimum number of compatible signals needed before the system is
   allowed to form a structural pressure candidate for v1?
