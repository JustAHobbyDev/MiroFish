# Capital Flow Signal Candidate v1

Date: March 20, 2026

## Purpose

Define the first atomic discovery object in the upstream workflow.

A `capital_flow_signal_candidate` is:

- weaker than a thesis
- weaker than a bounded universe
- weaker than a structural pressure candidate

It is the smallest normalized public observation that may imply directional
capital flow into a real system.

This spec is deliberately narrow.

It covers:

- first-pass interpretation of possible capital-flow implications from one
  artifact at a time
- rising-demand structural pressure only

It does not yet cover:

- constrained-access archetypes
- legal exclusivity
- reimbursement gating
- downstream bottleneck verification

## Why This Object Exists

The system needs a unit smaller than `structural_pressure_candidate`.

Reason:

1. a structural pressure candidate should never be formed from one article,
   filing, release, or post
2. but the system still needs to preserve individual observations in a reusable
   way
3. the first useful judgment is not “is this the thesis?”
4. it is “does this artifact plausibly imply directional capital flow?”

So the workflow should begin with:

1. raw public information
2. `capital_flow_signal_candidate`
3. `structural_pressure_candidate`
4. bounded universe

## Facts

1. Useful capital-flow evidence is often indirect.

2. A source may imply directional capital flow without using words like:
   - `capital`
   - `investment`
   - `capex`

3. Indirect examples include:
   - factory expansion
   - supply agreements
   - procurement commitments
   - manufacturing line additions
   - demand-driven hiring ramps
   - architecture shifts that increase component intensity

4. The first interpretation pass should be blind to historical case context.

5. Therefore the first extraction object must be:
   - artifact-local
   - provenance-preserving
   - auditable

## Assumptions

1. The first useful narrowing clue comes from directional capital-flow
   implications, not from prior company or industry conviction.

2. The first v1 implementation should optimize for industrial demand pressure,
   not broad universal news understanding.

3. The interpretation pass should see only:
   - the artifact
   - minimal provenance
   - a fixed prompt

4. It should not see:
   - prior cluster state
   - benchmark notes
   - historical success cases

## Non-Goals

This object is not trying to answer:

1. whether the thesis is true
2. whether the system is definitely bottlenecked
3. which company is the best expression
4. whether the market is mispricing the situation
5. what the final bounded universe should be

Those are downstream.

## Definition

A `capital_flow_signal_candidate` is a normalized public observation that may
indicate:

- planned capital deployment
- current capital deployment
- procurement pull
- demand-induced capacity response
- architecture-driven intensity increase
- policy-enabled buildout

even when the artifact does not explicitly mention capital allocation.

It is stronger than:

- raw source text
- an isolated headline
- an unstructured ticker mention

It is weaker than:

- a structural pressure candidate

## Required Invariants

Every valid `capital_flow_signal_candidate` must have all of these:

1. `Source provenance`
   - exact source reference
   - source class
   - time boundary

2. `Observable statement`
   - one concrete fact, event, claim, or observation
   - not a broad narrative summary

3. `Capital-flow implication`
   - one plain-language explanation of how the artifact may imply directional
     resource deployment or physical buildout

4. `Observation directness`
   - whether the implication is:
     - `direct`
     - `indirect`

5. `System hint`
   - a provisional hint about the affected system, component family, process,
     or industrial area

If any invariant fails, the object should not exist.

## Design Rules

### Atomicity

A `capital_flow_signal_candidate` should contain:

- one observation
- one dominant interpretation

If a source contains three materially different observations, split them into
three candidates.

### Zero-context interpretation

The extraction pass must be performed with:

1. the artifact body
2. minimal provenance
3. the fixed extraction prompt

It must not use:

1. prior cluster state
2. prior artifacts
3. historical benchmark knowledge
4. known winning tickers

### Scope discipline

Do not let the object turn into:

- a chain map
- a bottleneck claim
- a candidate-expression memo

That is premature.

## Supported Capital-Flow Implication Types v1

Keep the first type set narrow.

### `direct_capital_allocation`

Use when:

- the artifact directly states spend, capex, financing, awards, or facility
  investment

### `procurement_or_commitment_pull`

Use when:

- the artifact implies meaningful demand through procurement, supply
  commitments, customer orders, or qualification pull

### `capacity_response`

Use when:

- a company or supplier adds facilities, lines, tooling, or output because
  demand is increasing

### `architecture_induced_intensity`

Use when:

- a design or deployment shift increases component, material, or process
  intensity in a way likely to drive future spend or buildout

### `policy_enabled_buildout`

Use when:

- policy, subsidy, regulation, or public support directly increases likely
  buildout or deployment

## Minimal Shape

This is not final storage schema.
It is the minimum working contract.

```json
{
  "capital_flow_signal_id": "cfs_photonics_2025_12_01_001",
  "as_of_date": "2025-12-01",
  "source_class": "investor_post",
  "source_ref": {
    "platform": "x",
    "author": "aleabitoreddit",
    "post_id": "..."
  },
  "observable_statement": "LITE is directly correlated to TPU ramp up.",
  "capital_flow_implication_type": "procurement_or_commitment_pull",
  "observation_directness": "indirect",
  "capital_flow_implication": "If TPU deployment is ramping, optical networking and adjacent photonics layers may absorb follow-on spend and procurement.",
  "system_hints": [
    "AI photonics",
    "TPU networking"
  ],
  "physical_implication": "Rising AI-network deployment may increase physical demand for optical components and upstream inputs.",
  "confidence": "low"
}
```

## Required Fields

### Identity

1. `capital_flow_signal_id`
2. `as_of_date`
3. `source_class`
4. `source_ref`

### Core observation

1. `observable_statement`
2. `capital_flow_implication_type`
3. `observation_directness`
4. `capital_flow_implication`

### Discovery hints

1. `system_hints`
2. `physical_implication`
3. `confidence`

## Confidence Bands

These are workflow bands, not final scoring outputs.

### `low`

Use when:

- the implication is plausible but indirect
- the source is weak or socially synthesized

### `medium`

Use when:

- the artifact contains a concrete observation with a clear capital-flow
  implication
- the system hint is reasonably grounded

### `high`

Use when:

- the source directly states spend, expansion, commitments, or buildout
- the implication is explicit and not heavily inferred

## Source Rules

### Allowed to produce capital-flow signal candidates

1. company filings
2. earnings releases and transcripts
3. company press releases
4. policy or government notices
5. trade press
6. technical or manufacturing announcements
7. investor posts

### Not sufficient on their own for downstream narrowing

1. a single investor post
2. a single media article
3. a single price move
4. vague theme chatter

Those may create a valid `capital_flow_signal_candidate`.
They are not enough to create a `structural_pressure_candidate`.

## Promotion Rules

### Raw public information -> capital_flow_signal_candidate

Promote when all are true:

1. one concrete observation can be isolated
2. the artifact implies possible directional capital flow or physical buildout
3. at least one system hint can be named

### capital_flow_signal_candidate -> reject

Reject when any are true:

1. the artifact is purely opinion with no concrete observation
2. there is no plausible directional capital-flow implication
3. the implication depends on outside historical knowledge rather than the
   artifact itself

## Example Interpretation Boundary

Valid:

- “This factory expansion likely reflects rising demand and future capital
  deployment into this manufacturing layer.”

Invalid:

- “This means AXTI is the bottleneck and will outperform.”

The first is a capital-flow implication.
The second is a thesis leap.

## Relationship To MiroFish

If MiroFish is used here, its useful role is not historical memory during first
pass interpretation.

Its useful role would be:

1. storing isolated artifacts with provenance
2. presenting one artifact at a time to the model
3. preserving the extracted candidate object for later clustering

That is compatible with zero-context first-pass interpretation.

## Next Step

The next needed artifact is:

- [2026-03-20-capital-flow-signal-extraction-spec-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-20-capital-flow-signal-extraction-spec-v1.md)

That should define the fixed prompt and output contract for artifact-local
extraction.
