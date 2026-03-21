# Bounded Universe Expansion Rules v1

Date: March 21, 2026

## Purpose

Define the deterministic step from:

1. `bounded_universe_candidate`
2. to a bounded research-expansion plan

This is the first downstream step after a pressure lane is promotion-ready.

## Facts

1. A bounded universe is still not a ticker list.
2. The next step should stay inside the bounded lane.
3. Expansion should be auditable and source-prioritized.

## Assumptions

1. v1 should use deterministic templates, not model-generated search plans.
2. The first template should support the transformer/grid-equipment universe.
3. Expansion plans should name both:
   - what to search
   - what to avoid

## Required Outputs

Every `bounded_universe_expansion_plan` should include:

1. `origin_bounded_universe_candidate_id`
2. `system_label`
3. `expansion_objective`
4. `entity_lane_hints`
5. `query_seed_terms`
6. `negative_boundaries`
7. `first_actions`
8. `source_classes_priority`
9. `suspected_stress_layers`
10. `confidence`

## Rule

The expansion plan must stay inside the bounded system label and stress layers.

It should:

1. enumerate likely entity lanes
2. prioritize the next source classes
3. include negative boundaries so the search does not drift into generic macro or unrelated industrial material

## First Supported Template

### `grid equipment and transformer buildout`

Entity lanes:

1. transformer manufacturers
2. switchgear manufacturers
3. substation equipment suppliers
4. grid equipment component suppliers
5. core, coil, insulation, and conductor input suppliers

## Open Questions

1. Should v1 expansion plans also carry explicit review queries for each source class?
2. Should visible-beneficiary hints become mandatory before expansion planning?
