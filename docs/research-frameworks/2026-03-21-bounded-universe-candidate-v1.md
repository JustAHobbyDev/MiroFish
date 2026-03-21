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

## Promotion Preconditions

Promote a `structural_pressure_candidate` into a
`bounded_universe_candidate` only when all are true:

1. `source_diversity_corroboration_satisfied = true`
2. `bounded_universe_promotion_ready = true`
3. the candidate names a concrete system or supply-layer lane
4. the next research expansion can be expressed as a bounded search space

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

## Non-Goals

This object is not trying to:

1. identify the best public company
2. rank expressions
3. prove the final bottleneck
4. decide valuation or mispricing

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
