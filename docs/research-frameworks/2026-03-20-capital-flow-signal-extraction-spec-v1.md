# Capital Flow Signal Extraction Spec v1

Date: March 20, 2026

## Purpose

Define the first extraction pass that turns one artifact into zero or more
`capital_flow_signal_candidate` objects.

This extraction pass is intentionally blind.

It exists to answer:

- does this artifact, by itself, plausibly imply directional capital flow into
  a real system?

It does not exist to answer:

- is this the right thesis?
- is this the right industry?
- is this the right stock?

## Core Principle

Interpret one artifact at a time with zero historical context.

The model may use:

1. the artifact body
2. minimal provenance
3. the fixed prompt

The model may not use:

1. prior artifacts
2. prior cluster state
3. known benchmark cases
4. known successful tickers
5. any retrieved external context

## Facts

1. Useful capital-flow evidence is often indirect.

2. A source may imply directional buildout or procurement without saying
   `investment`, `capital`, or `capex`.

3. Therefore extraction must interpret implication, not only explicit wording.

4. If the model sees prior context, it will over-interpret weak artifacts.

5. The first pass must bias toward auditable local interpretation.

## Assumptions

1. The same artifact may yield:
   - zero candidates
   - one candidate
   - multiple candidates

2. Multiple candidates should be rare and only used when the artifact contains
   clearly separable observations.

3. The extraction pass should preserve uncertainty rather than force a signal.

## Non-Goals

This spec is not defining:

1. clustering logic
2. promotion thresholds
3. bounded-universe formation
4. bottleneck verification
5. final company selection

## Input Contract

Each extraction call receives exactly one normalized artifact.

### Required input fields

1. `artifact_id`
2. `source_class`
3. `publisher_or_author`
4. `published_at`
5. `title`
6. `body_text`
7. `source_url`

## Output Contract

The extraction output must be valid JSON with this shape:

```json
{
  "artifact_id": "artifact_123",
  "produced_candidates": true,
  "candidates": [
    {
      "observable_statement": "...",
      "capital_flow_implication_type": "capacity_response",
      "observation_directness": "indirect",
      "capital_flow_implication": "...",
      "system_hints": [
        "..."
      ],
      "physical_implication": "...",
      "confidence": "medium"
    }
  ],
  "rejection_reason": null
}
```

If no candidate should be produced:

```json
{
  "artifact_id": "artifact_123",
  "produced_candidates": false,
  "candidates": [],
  "rejection_reason": "No plausible directional capital-flow implication can be inferred from the artifact alone."
}
```

## Output Rules

### Candidate count

1. prefer `0` or `1`
2. use `2+` only when the artifact contains clearly separate observations
3. do not split one idea into multiple near-duplicate candidates

### Statement rule

`observable_statement` must be:

1. concrete
2. artifact-local
3. phrased as an observation, not a thesis

### Implication rule

`capital_flow_implication` must explain:

1. what directional flow or buildout may be implied
2. why that implication follows from the artifact

It must not claim:

1. the final bottleneck
2. the final best expression
3. a market mispricing conclusion

### Directness rule

Use:

1. `direct`
   - if the artifact explicitly states spend, expansion, orders, awards,
     commitments, or buildout
2. `indirect`
   - if the implication must be inferred from demand pull, architecture shift,
     qualification, or similar signals

### Confidence rule

Confidence is about the local observation and implication quality.

It is not about:

1. eventual investment quality
2. confidence in a later thesis

## Allowed Implication Types v1

1. `direct_capital_allocation`
2. `procurement_or_commitment_pull`
3. `capacity_response`
4. `architecture_induced_intensity`
5. `policy_enabled_buildout`

## Fixed Extraction Prompt v1

### System prompt

You are extracting possible capital-flow implications from a single public
artifact.

Use only the artifact and its provenance.

Do not use prior knowledge about historical winners, bottlenecks, companies,
themes, or the broader corpus.

Your job is not to form a thesis.

Your job is to decide whether this artifact alone contains one or more concrete
observations that plausibly imply directional capital flow, procurement pull,
capacity response, or physical buildout in a real system.

If no such implication is plausible from the artifact alone, return no
candidates.

Return strict JSON only.

### User prompt template

```text
Artifact metadata:
- artifact_id: {artifact_id}
- source_class: {source_class}
- publisher_or_author: {publisher_or_author}
- published_at: {published_at}
- title: {title}
- source_url: {source_url}

Artifact body:
{body_text}

Task:
1. Determine whether this artifact alone implies possible directional capital
   flow into a real system.
2. If yes, extract up to 3 capital_flow_signal_candidate objects.
3. Each candidate must contain:
   - observable_statement
   - capital_flow_implication_type
   - observation_directness
   - capital_flow_implication
   - system_hints
   - physical_implication
   - confidence
4. Do not mention specific stocks as the answer unless the artifact itself is
   explicitly about them.
5. Do not infer a bottleneck or market mispricing.
6. If the artifact does not plausibly imply directional capital flow from the
   artifact alone, return no candidates.
```

## Acceptance Criteria

An extraction is valid only if all are true:

1. candidate objects are artifact-local
2. no historical benchmark reasoning appears
3. no ticker-picking language appears unless present in the artifact itself
4. no bottleneck conclusion appears
5. implications are directional and physically interpretable

## Failure Modes

Reject or flag outputs that do any of these:

1. paraphrase the artifact without any directional implication
2. jump from one weak observation to a full thesis
3. import outside context
4. confuse market narrative with physical buildout
5. emit too many low-quality candidates from one artifact

## Relationship To MiroFish

MiroFish could be useful here if it acts as an artifact boundary layer.

That means:

1. one artifact is stored with provenance
2. one extraction prompt is run against that artifact only
3. the result is stored as a first-pass candidate object

That is useful.

What would not be useful at this stage:

1. feeding historical case memory into the extraction prompt
2. feeding prior cluster context into the extraction prompt
3. letting prior successful theses influence first-pass interpretation

## Next Step

After this extraction spec, the next needed artifact is:

- promotion logic from `capital_flow_signal_candidate` to
  `structural_pressure_candidate`
