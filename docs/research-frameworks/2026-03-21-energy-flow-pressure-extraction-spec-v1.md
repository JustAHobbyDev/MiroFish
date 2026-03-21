# Energy Flow Pressure Extraction Spec v1

Date: March 21, 2026

## Purpose

Define the first extraction pass that turns one artifact into zero or more
`energy_flow_pressure_signal` objects.

This extraction pass is intentionally blind.

It exists to answer:

- does this artifact, by itself, plausibly indicate rising pressure on an
  energy system as a necessary production input?

It does not exist to answer:

- is this the final thesis?
- is this the final bottleneck?
- which company is the best expression?

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

1. Useful energy-pressure evidence is often upstream of direct capital
   allocation.

2. An artifact can imply real future infrastructure need without stating:
   - capex
   - financing
   - construction

3. Utility pipeline, load-growth, and generation-demand articles often carry
   strong physical-system implications even when they fail the direct
   `capital_flow_signal_candidate` gate.

4. Therefore extraction must preserve:
   - physical-demand pressure
   - while not pretending that capital is already committed

## Assumptions

1. The same artifact may yield:
   - zero `energy_flow_pressure_signal`s
   - one `energy_flow_pressure_signal`
   - rarely more than one

2. Candidate count should still prefer:
   - `0`
   - `1`

3. The extraction pass should preserve the distinction between:
   - `energy_flow_pressure_only`
   - `energy_flow_pressure_and_capital_flow`

## Non-Goals

This spec is not defining:

1. clustering logic
2. promotion thresholds
3. bounded-universe formation
4. bottleneck verification
5. general production-input extraction beyond energy

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
      "energy_pressure_type": "load_growth",
      "observation_directness": "direct",
      "energy_flow_implication": "...",
      "system_hints": [
        "..."
      ],
      "physical_implication": "...",
      "relationship_to_capital_flow": "energy_flow_pressure_only",
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
  "rejection_reason": "No plausible energy-system pressure implication can be inferred from the artifact alone."
}
```

## Output Rules

### Candidate count

1. prefer `0` or `1`
2. use `2+` only when the artifact contains clearly separate energy-pressure
   observations
3. do not split one idea into multiple near-duplicate candidates

### Statement rule

`observable_statement` must be:

1. concrete
2. artifact-local
3. phrased as an observation, not a thesis

### Implication rule

`energy_flow_implication` must explain:

1. what energy-system pressure is implied
2. why that implication follows from the artifact

It must not claim:

1. the final bottleneck
2. the final best expression
3. a market mispricing conclusion

### Directness rule

Use:

1. `direct`
   - if the artifact explicitly states load growth, pipeline growth, approved
     generation additions, capacity strain, or equivalent pressure
2. `indirect`
   - if the pressure must be inferred from adjacent operational facts

### Relationship-to-capital-flow rule

Use:

1. `energy_flow_pressure_only`
   - if the artifact indicates rising energy pressure without direct capital
     commitment
2. `energy_flow_pressure_and_capital_flow`
   - if the artifact indicates both:
     - energy-system pressure
     - and direct capital-flow evidence such as spending plan, financing,
       signed deal, siting, procurement, or construction

### Confidence rule

Confidence is about the local observation and implication quality.

It is not about:

1. eventual investment quality
2. confidence in a later thesis

## Allowed Pressure Types v1

1. `load_growth`
2. `pipeline_pressure`
3. `capacity_tightness`
4. `infrastructure_response_need`

## Fixed Extraction Prompt v1

### System prompt

You are extracting possible energy-system pressure implications from a single
public artifact.

Use only the artifact and its provenance.

Do not use prior knowledge about historical winners, bottlenecks, companies,
themes, or the broader corpus.

Your job is not to form a thesis.

Your job is to decide whether this artifact alone contains one or more concrete
observations that plausibly imply rising pressure on an energy system as a
necessary production input.

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
1. Determine whether this artifact alone implies possible pressure on an energy
   system as a necessary production input.
2. If yes, extract up to 3 energy_flow_pressure_signal objects.
3. Each candidate must contain:
   - observable_statement
   - energy_pressure_type
   - observation_directness
   - energy_flow_implication
   - system_hints
   - physical_implication
   - relationship_to_capital_flow
   - confidence
4. Use relationship_to_capital_flow:
   - energy_flow_pressure_only
   - or energy_flow_pressure_and_capital_flow
5. Do not infer a bottleneck or market mispricing.
6. If the artifact does not plausibly imply energy-system pressure from the
   artifact alone, return no candidates.
```

## Acceptance Criteria

An extraction is valid only if all are true:

1. candidate objects are artifact-local
2. no historical benchmark reasoning appears
3. no ticker-picking language appears unless present in the artifact itself
4. no bottleneck conclusion appears
5. energy-pressure implications are physically interpretable
6. `relationship_to_capital_flow` is justified by the artifact itself

## Failure Modes

Reject or flag outputs that do any of these:

1. confuse generic energy narrative with concrete energy-system pressure
2. treat every utility mention as energy pressure
3. jump from load-growth narrative to full capex certainty without evidence
4. import outside context
5. duplicate the same observation into multiple candidates

## Decision Rule

For now:

- implement this extraction contract only for `energy_flow_pressure_signal`

Do not generalize the prompt or schema yet to:

- `production_input_pressure_signal`

Reason:

1. energy is the only production-input class currently tested on real batch
   artifacts
2. broader generalization would introduce unsupported schema branches
