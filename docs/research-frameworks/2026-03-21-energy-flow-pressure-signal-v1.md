# Energy Flow Pressure Signal v1

Date: March 21, 2026

## Purpose

Define a new upstream discovery object for real artifacts that:

- do not yet qualify as direct `capital_flow_signal_candidate`s
- but do indicate rising physical pressure in energy as a production input

This spec is deliberately narrow.

It covers:

- electricity-load growth
- utility pipeline growth
- power-system demand pressure
- energy-input pressure from rising industrial or data-center demand

It does not yet cover:

- water pressure
- cooling pressure
- feedstock pressure
- labor pressure
- logistics pressure
- a generalized `production_input_pressure_signal`

## Why This Object Exists

The final `trade_press` benchmark exposed a real distinction.

Some review-stage utility artifacts were:

- weak direct capital-flow artifacts
- strong physical-demand artifacts

Examples:

- `PG&E data center pipeline swells to 10GW`
- `US utility Exelon reports data center pipeline of 33GW`
- `FirstEnergy expects peak load to grow 45% by 2035 on data centers`

These should not be promoted as direct capital-flow candidates on their own.

But they should also not be discarded.

They preserve an earlier upstream state:

- a necessary production input is coming under pressure
- future capital response is likely
- but not yet concretely committed in the artifact

That is what this object captures.

## Facts

1. Energy is a necessary input to production.

2. Rising energy demand can imply later capital deployment into:
   - generation
   - transmission
   - substations
   - transformers
   - cooling and adjacent infrastructure

3. Energy-flow pressure is not identical to capital flow.

4. A headline can strongly imply energy-system stress without proving:
   - committed spend
   - signed procurement
   - financing
   - construction

5. The `trade_press` test showed a coherent set of such artifacts.

## Assumptions

1. The first non-capital upstream pressure object should be energy-specific,
   not fully generalized.

2. Energy pressure is the highest-value production-input case currently
   supported by the benchmark evidence.

3. Generalizing too early into `production_input_pressure_signal` would add
   abstraction before we have equivalent evidence for:
   - water
   - cooling
   - labor
   - logistics

## Non-Goals

This object is not trying to answer:

1. whether direct capital has already been committed
2. whether a bottleneck is verified
3. which company is the best expression
4. whether the market is mispricing the setup
5. whether the system should already form a bounded universe by itself

Those remain downstream.

## Definition

An `energy_flow_pressure_signal` is a normalized artifact-local observation
that indicates rising pressure on an energy system as a necessary production
input.

It is stronger than:

- raw source text
- a generic narrative mention of power demand

It is weaker than:

- a `capital_flow_signal_candidate`
- a `structural_pressure_candidate`

## Required Invariants

Every valid `energy_flow_pressure_signal` must have all of these:

1. `Source provenance`
   - exact source reference
   - source class
   - time boundary

2. `Observable energy-pressure statement`
   - one concrete observation about:
     - load growth
     - demand pipeline
     - energy-system capacity pressure
     - power-related constraint or expected stress

3. `Production-input grounding`
   - the signal must be tied to an energy system, not only a financial or
     thematic narrative

4. `Physical implication`
   - one plain-language explanation of how the artifact implies energy-system
     pressure or future infrastructure need

5. `Observation directness`
   - whether the artifact states the energy-pressure observation directly or
     only implies it

If any invariant fails, the object should not exist.

## Design Rules

### Atomicity

An `energy_flow_pressure_signal` should contain:

- one observation
- one dominant interpretation

Do not turn it into:

- a utility-capex thesis
- a bottleneck memo
- a full system map

### Zero-context interpretation

Like `capital_flow_signal_candidate`, this object should be formed:

1. from one artifact at a time
2. with minimal provenance
3. without historical cluster context

### Relationship to capital flow

This object is allowed to exist in two modes:

1. `energy_flow_pressure_only`
   - the artifact implies physical energy pressure
   - but does not yet justify direct capital-flow promotion

2. `energy_flow_pressure_and_capital_flow`
   - the artifact implies energy pressure
   - and also qualifies as direct capital-flow evidence

Example:

- `DTE inks first data center deal to grow electric load 25%`
  can legitimately carry both roles

## Supported Pressure Subtypes v1

Keep the first subtype set narrow.

### `load_growth`

Use when:

- the artifact states or implies large electricity-load growth

### `pipeline_pressure`

Use when:

- the artifact describes a large utility or project pipeline likely to raise
  future energy demand

### `capacity_tightness`

Use when:

- the artifact indicates the energy system is becoming tight, constrained, or
  stressed

### `infrastructure_response_need`

Use when:

- the artifact implies future need for:
  - grid upgrades
  - transformers
  - substations
  - generation additions

## Minimal Shape

```json
{
  "energy_flow_pressure_signal_id": "efps_utility_2026_03_21_001",
  "as_of_date": "2026-03-21",
  "source_class": "trade_press",
  "source_ref": {
    "publication": "Utility Dive",
    "url": "https://example.com/article"
  },
  "observable_statement": "PG&E data center pipeline swells to 10GW.",
  "energy_pressure_type": "pipeline_pressure",
  "observation_directness": "direct",
  "energy_flow_implication": "Expected data-center demand is likely to place substantial pressure on the utility power system.",
  "system_hints": [
    "utility grid",
    "data center power demand"
  ],
  "physical_implication": "If the pipeline converts, generation, transmission, substation, and transformer capacity may need to expand.",
  "relationship_to_capital_flow": "energy_flow_pressure_only",
  "confidence": "medium"
}
```

## Required Fields

### Identity

1. `energy_flow_pressure_signal_id`
2. `as_of_date`

### Core interpretation

1. `observable_statement`
2. `energy_pressure_type`
3. `observation_directness`
4. `energy_flow_implication`
5. `physical_implication`

### Context

1. `source_class`
2. `source_ref`
3. `system_hints`
4. `relationship_to_capital_flow`
5. `confidence`

## Source Rules

### Especially relevant for v1

1. trade press
2. utility reporting
3. company releases about utility load or power demand
4. government or utility-planning notices where physical energy pressure is
   explicit

### Not sufficient on their own

1. generic AI-power commentary without concrete load or pipeline signal
2. broad macro energy narrative
3. price action alone
4. vague “power demand is rising” language without artifact-local grounding

## Promotion Rules

### Raw public information -> energy_flow_pressure_signal

Promote when all are true:

1. the artifact contains a concrete energy-system demand or pressure signal
2. the signal is grounded in a real physical system
3. the artifact plausibly implies future infrastructure response or system
   stress

### energy_flow_pressure_signal -> capital_flow_signal_candidate

Do not auto-promote.

Promotion requires additional evidence such as:

1. explicit spending plan
2. financing
3. signed procurement or offtake
4. facility siting
5. construction or physical buildout

### energy_flow_pressure_signal -> structural_pressure_candidate

May contribute, but should not dominate alone.

It should combine with:

1. `capital_flow_signal_candidate`s
2. direct capacity-response artifacts
3. shortage or infrastructure-response evidence

## Decision On Generalization

For v1:

- keep the object energy-specific

Do not generalize yet to:

- `production_input_pressure_signal`

Reason:

1. the current benchmark evidence is strongest for energy
2. we do not yet have equally strong tested cases for:
   - water
   - cooling
   - labor
   - logistics
3. abstraction should follow evidence, not lead it

## Recommendation

Implement:

- `energy_flow_pressure_signal`

Defer:

- `production_input_pressure_signal`

until at least one more non-energy production-input class is tested against
real artifacts.
