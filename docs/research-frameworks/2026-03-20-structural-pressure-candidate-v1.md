# Structural Pressure Candidate v1

Date: March 20, 2026

## Purpose

Define the first upstream discovery object for the product:

- not a thesis
- not a ticker
- not a bounded universe

The goal of this object is to capture early evidence that rising demand is
likely to create physical bottlenecks somewhere in a system.

This spec is deliberately narrow.

It covers:

- structural pressure from rising demand

It does not yet cover:

- patent or legal exclusivity
- reimbursement-driven access constraints
- regulatory gating
- other constrained-access archetypes

## Why This Object Exists

The product currently starts too far downstream.

Objects like:

- thesis intake
- candidate output
- ranking logic

all assume that the system already knows what deserves deep investigation.

That is the wrong starting point.

The first useful object should answer:

- is there enough recurring public evidence to believe a real physical system
  is coming under pressure from rising demand?

If yes:

- the system earns the right to form a bounded universe and do deeper work

## Facts

1. The `AXTI` replay suggests the process did not start with `AXTI`.

2. The earlier useful state looked more like:
   - TPU and hyperscaler buildout pressure
   - photonics demand pressure
   - visible beneficiaries like `LITE`

3. That means the earlier object was something like:
   - a growing sense of structural pressure in a system

4. The system needs an explicit object for that state before:
   - visible beneficiary identification
   - chain expansion
   - bottleneck verification

5. This object should be formed from multiple upstream signals, primarily:
   - `capital_flow_cluster`
   - and, where relevant, `energy_flow_pressure_cluster`
   not from raw mention volume alone.

## Assumptions

1. Rising-demand bottlenecks can often be detected from repeated public
   observations before the best expression is obvious.

2. Public information is noisy, so a single article or post should never create
   a structural pressure candidate on its own.

3. The first useful promotion should be from broad public flow to a provisional
   demand-pressure object, not directly to a thesis.

4. The first v1 implementation should prefer industrial and physical systems
   over broader abstract narratives.

## Non-Goals

This object is not trying to answer:

1. which company is the best expression
2. whether the market is definitively mispricing the thesis
3. whether the bottleneck is already fully verified
4. what options structure to use
5. whether this is a complete sector thesis

Those come later.

## Definition

A `structural_pressure_candidate` is a provisional research object that
represents:

- repeated public evidence of rising demand
- affecting a real physical system
- in a way that plausibly creates upstream bottlenecks or capacity stress

It is stronger than:

- isolated signal detection

It is weaker than:

- a verified bottleneck thesis

## Required Invariants

Every valid `structural_pressure_candidate` must have all of these:

1. `Repeated demand evidence`
   - more than one public signal indicates rising demand, buildout, adoption, or
     spend

2. `Physical system grounding`
   - the pressure is attached to a real system, supply chain, or industrial
     process, not only a financial narrative

3. `Stress rationale`
   - there is a clear reason to suspect that rising demand could create
     bottlenecks, lead-time stress, capacity tightness, or concentrated supplier
     dependence

4. `Time boundary`
   - all supporting evidence is bounded by an explicit as-of date or rolling
     window

5. `Source provenance`
   - every supporting signal must be traceable to a public source

If any invariant fails, the object should not exist.

## Minimal Shape

This is not final storage schema.
It is the minimum working contract.

```json
{
  "pressure_candidate_id": "spc_photonics_2025_12_22_v1",
  "as_of_date": "2025-12-22",
  "status": "candidate",
  "pressure_type": "rising_demand",
  "system_label": "AI photonics buildout",
  "demand_driver_summary": "Hyperscaler TPU and AI-network buildout is increasing demand for photonics infrastructure.",
  "pressure_statement": "Rising AI optical demand is likely to stress component, material, and supplier layers upstream of visible beneficiaries.",
  "supporting_capital_flow_signal_ids": [
    "cfs_001",
    "cfs_002",
    "cfs_003"
  ],
  "signal_count": 3,
  "likely_visible_beneficiaries": [
    "LITE",
    "COHR"
  ],
  "suspected_stress_layers": [
    "optical components",
    "laser supply",
    "InP-related materials"
  ],
  "formation_basis": {
    "repeated_demand_signals": true,
    "physical_system_grounded": true,
    "stress_rationale_present": true
  },
  "confidence": "medium"
}
```

## Required Fields

### Identity

1. `pressure_candidate_id`
2. `as_of_date`
3. `status`

### Core interpretation

1. `pressure_type`
   - fixed to `rising_demand` for v1
2. `system_label`
3. `demand_driver_summary`
4. `pressure_statement`

### Evidence

1. `supporting_capital_flow_signal_ids`
2. `signal_count`
3. `source_classes`
4. `time_window` or `as_of_date`

### Discovery hints

1. `likely_visible_beneficiaries`
2. `suspected_stress_layers`
3. `formation_basis`
4. `confidence`
5. `source_diversity_status`
6. `requires_source_diversity_corroboration`
7. `source_diversity_corroboration_satisfied`
8. `boundedness_status`
9. `requires_system_narrowing`
10. `bounded_universe_promotion_ready`

## Source Rules

### Allowed to contribute to formation

1. `capital_flow_cluster`
2. `energy_flow_pressure_cluster`

### Not sufficient on their own

1. a single investor post
2. a single media article
3. a single price move
4. vague theme chatter

### Formation rule

At least one valid upstream cluster should support formation.

Preferred composition:

1. at least one `capital_flow_cluster`
2. optionally one overlapping `energy_flow_pressure_cluster`
3. at least one contributing cluster should tie the pressure to a real system or
   buildout lane

## Promotion Rules

### Broad public flow -> structural pressure candidate

Promote when all are true:

1. a valid upstream cluster exists
2. the system can name the affected physical system
3. there is a plausible stress rationale
4. if both cluster types exist, they are compatible on system, geography, or
   demand story

### Cluster merge -> structural pressure candidate

Merge a `capital_flow_cluster` and an `energy_flow_pressure_cluster` into one
`structural_pressure_candidate` when all are true:

1. they overlap on a concrete system label or adjacent system labels
2. they share a compatible time window
3. they do not conflict on direction
4. the merged statement is stronger than either cluster alone

If only one cluster type exists:

1. a `capital_flow_cluster` may form a `structural_pressure_candidate` alone
   when system grounding and stress rationale are already clear
2. an `energy_flow_pressure_cluster` alone should usually remain upstream unless
   it also contains strong infrastructure-response evidence

Detailed merge policy now lives in:

- `2026-03-21-structural-pressure-merge-rules-v1.md`

### Single-source corroboration rule

If only one source class supports the candidate:

1. the candidate may still exist
2. confidence should be capped at `medium`
3. `source_diversity_status` should be `single_source_class`
4. `requires_source_diversity_corroboration` should be `true`

Corroboration is only considered satisfied in v1 when:

1. the candidate has at least `2` distinct source classes
2. at least one supporting `capital_flow_cluster` is present

Satisfying corroboration does not make the candidate promotion-ready by itself.
The system label and stress zone must still be concrete enough to bound a
review universe.

## Boundedness Rule

Even corroborated candidates should remain gated if the system label is still
too broad.

Examples that are usually bounded enough in v1:

1. `grid equipment and transformer pressure`
2. `data center power demand buildout`
3. `utility and large-load power demand pressure`

Examples that are still too broad in v1:

1. `industrial manufacturing expansion`
2. `power generation and backup equipment pressure`
3. `general industrial buildout`

### Structural pressure candidate -> bounded universe

Promote when all are true:

1. at least one likely visible beneficiary is identified
2. at least one suspected stress layer is named
3. the system can specify which source classes are now worth deeper review
4. any required source-diversity corroboration has been satisfied, or the
   candidate has been explicitly promoted by an analyst
5. the candidate is bounded enough to support a review universe, or the
   candidate has been explicitly promoted by an analyst

### Structural pressure candidate -> reject

Reject when any are true:

1. the evidence collapses to generic macro excitement
2. the affected system cannot be named concretely
3. the stress rationale is only narrative and has no physical basis
4. later signals suggest demand pressure was temporary or misread

## Confidence Bands

These are workflow bands, not final scoring outputs.

### `low`

- repeated attention exists
- but physical system grounding is still weak

### `medium`

- repeated demand evidence exists
- physical system is identifiable
- likely visible beneficiaries are emerging

### `high`

- demand pressure is persistent
- physical system is clear
- likely visible beneficiaries and suspected stress layers are both concrete
- source diversity corroboration is present

High confidence does not mean verified bottleneck.
It only means the candidate deserves bounded-universe formation.

## Example: Photonics

### Inputs

As-of `2025-12-22`, repeated public evidence suggests:

1. TPU / AI buildout is rising
2. optical networking / photonics demand is rising
3. `LITE` and `COHR` are visible beneficiaries
4. upstream supply-chain dependence may matter

### Valid candidate

`system_label`

- `AI photonics buildout`

`pressure_statement`

- `Rising AI optical demand is likely to stress upstream photonics component and materials layers.`

`likely_visible_beneficiaries`

- `LITE`
- `COHR`

`suspected_stress_layers`

- `optical components`
- `laser supply`
- `InP-related materials`

This is a valid `structural_pressure_candidate` even before `AXTI` is fully
verified as the bottleneck expression.

That is the whole point of the object.

## Example: Invalid Candidate

`AI is hot and lots of companies mention it`

Why invalid:

1. no concrete physical system
2. no stress rationale
3. no visible-beneficiary orientation
4. no suspected stress layers

This is theme enthusiasm, not structural pressure.

## Workflow Position

The intended sequence is:

1. broad public flow
2. signal candidates
3. `capital_flow_cluster`
4. `energy_flow_pressure_cluster`
5. `structural_pressure_candidate`
6. bounded universe formation
7. visible beneficiary confirmation
8. chain expansion
9. bottleneck candidate
10. verification
11. expression selection

## What This Enables

Once this object exists, the system can:

1. justify why it is narrowing into a universe
2. separate real physical pressure from vague thematic noise
3. track multiple competing pressure zones at once
4. benchmark whether the system noticed something early enough

## Failure Modes

1. `Generic excitement masquerading as pressure`
   - no system grounding

2. `System without stress`
   - system is real, but there is no reason to think rising demand creates a
     bottleneck

3. `Stress without provenance`
   - claim sounds plausible, but supporting signals are weak or untraceable

4. `Premature bottleneck leap`
   - the system jumps from demand pressure directly to a named bottleneck without
     bounded-universe formation and chain work

## Implementation Guidance

### Build first

1. signal normalization
2. per-lane clustering
3. physical-system labeling
4. minimal merge logic into `structural_pressure_candidate`

### Do not build first

1. deep expression ranking
2. options logic
3. rich chain-role subtype expansion
4. broad constrained-access generalization

## Relationship To Existing Artifacts

This object should sit upstream of:

- `thesis_intake`
- `source_bundle`
- `structural_parse`
- `theme_equity_decomposition`

It is the justification for why a research project should exist at all.

In other words:

- a thesis should be downstream of structural pressure detection, not the first
  thing the user has to invent.

## Open Questions

1. Should `structural_pressure_candidate` formation require one strong source
   class, or only multiple independent weak signals?

2. What is the first domain benchmark after photonics:
   - memory
   - transformers
   - rare earths

3. Should bounded-universe formation create a new project automatically, or
   stay as a pre-project object until analyst confirmation?
