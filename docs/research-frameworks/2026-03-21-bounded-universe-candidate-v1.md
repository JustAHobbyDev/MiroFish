# Bounded Universe Candidate v1

Date: March 21, 2026

## Purpose

Define the object that sits between:

1. `structural_pressure_candidate`
2. company-expression or ticker-specific research

This object exists so promotion-ready pressure does not jump straight into
ticker hunting.

## Facts

1. A structural-pressure object can be valid while still being too broad for
   direct company work.
2. Corroboration alone is not enough.
3. Boundedness alone is not enough.
4. The workflow needs an explicit object for:
   - the review universe
   - the reasons it was bounded
   - the source classes that should be expanded next

## Assumptions

1. v1 should stay upstream of ticker selection.
2. A bounded universe is a research set, not a ranking output.
3. The first bounded universes will usually be system or supply-layer oriented.

## Definition

A `bounded_universe_candidate` is a provisional research universe created from a
promotion-ready `structural_pressure_candidate`.

It should answer:

1. what system or layer is under pressure
2. what sub-layers should now be searched
3. which source classes justify the next expansion
4. what is still unresolved before expression ranking

## Exploratory Boundary

v1 also allows an `exploratory_candidate` status for a structural-pressure lane
that is:

1. already `bounded`
2. not yet promotion-ready
3. still suitable for research-set and entity-candidate formation

This is allowed only to support bounded downstream research. It does not
authorize bounded-universe promotion.

## Promotion Preconditions

Promote a `structural_pressure_candidate` into a
`bounded_universe_candidate` only when all are true:

1. `source_diversity_corroboration_satisfied = true`
2. `bounded_universe_promotion_ready = true`
3. the candidate names a concrete system or supply-layer lane
4. the next research expansion can be expressed as a bounded search space

## Exploratory Preconditions

Create an `exploratory_candidate` only when all are true:

1. `boundedness_status = bounded`
2. `requires_system_narrowing = false`
3. `bounded_universe_promotion_ready = false`
4. the lane is still concrete enough for deterministic expansion planning
5. the object remains explicitly blocked from promotion

## Minimal Shape

```json
{
  "bounded_universe_candidate_id": "buc_grid_transformer_pressure_2025_11_19_v1",
  "as_of_date": "2025-11-19",
  "status": "candidate",
  "origin_pressure_candidate_id": "spc_grid_equipment_and_transformer_buildout_2025-11-19_b00c1eaa",
  "universe_label": "grid equipment and transformer buildout universe",
  "system_label": "grid equipment and transformer buildout",
  "bounding_basis": {
    "source_diversity_corroborated": true,
    "system_bounded": true,
    "research_ready": true,
    "promotion_ready": true
  },
  "review_universe_definition": "Companies, suppliers, facilities, inputs, and public artifacts tied to transformer, switchgear, substation, and adjacent grid-equipment expansion.",
  "next_source_classes": [
    "company_release",
    "trade_press",
    "company_filing"
  ],
  "suspected_stress_layers": [
    "transformers",
    "switchgear",
    "substation equipment"
  ],
  "visible_beneficiary_hints": [],
  "confidence": "high"
}
```

## Required Fields

1. `bounded_universe_candidate_id`
2. `as_of_date`
3. `status`
4. `origin_pressure_candidate_id`
5. `universe_label`
6. `system_label`
7. `bounding_basis`
8. `review_universe_definition`
9. `next_source_classes`
10. `suspected_stress_layers`
11. `visible_beneficiary_hints`
12. `confidence`

`bounding_basis` should also include:

13. `research_ready`
14. `exploration_only`

## Non-Goals

This object is not trying to:

1. identify the best public company
2. rank expressions
3. prove the final bottleneck
4. decide valuation or mispricing

## Example Exploratory Case

### Valid Exploratory

`utility and large-load power buildout universe`

Why valid:

1. the lane is already bounded
2. deterministic downstream research can stay inside the lane
3. source-diversity corroboration is not yet strong enough for promotion

### Still Invalid

`power generation and backup equipment buildout universe`

Why still invalid:

1. the lane is still too broad
2. bounded downstream expansion would still over-widen the search space

## Example

### Valid

`grid equipment and transformer buildout universe`

Why valid:

1. mixed-source corroboration exists
2. the system is concrete
3. the next search space can be bounded to identifiable supply layers

### Invalid

`industrial manufacturing expansion universe`

Why invalid:

1. even with corroboration, the system is still too broad
2. the next search space is not yet narrowly expressible

## Open Questions

1. Should v1 bounded-universe formation require at least one named stress layer,
   not just a bounded system label?
2. Should the object include negative boundaries, such as what is explicitly out
   of scope for the first universe?
