# Bounded Research Set v1

Date: March 21, 2026

## Purpose

Define the first executable downstream object produced from a
`bounded_universe_expansion_plan`.

This object is the initial bounded research surface for later beneficiary,
supplier, and filing work.

## Facts

1. A bounded-universe candidate is still abstract.
2. An expansion plan names how to search.
3. A bounded research set should record what the deterministic search actually
   found in the local corpus.

## Definition

A `bounded_research_set` is the auditable output of executing a
`bounded_universe_expansion_plan` against a fixed local corpus.

It should include:

1. matched artifacts
2. matched source classes
3. extracted entity hints
4. coverage metrics

## Matching Rule

The execution step should require both:

1. bounded-plan term overlap
2. lane-anchor overlap derived from the bounded system label

This prevents a bounded research set from widening into adjacent but broader
capital-flow lanes.

## Required Fields

1. `bounded_research_set_id`
2. `origin_bounded_universe_expansion_plan_id`
3. `system_label`
4. `matched_artifacts`
5. `matched_artifact_ids`
6. `entity_candidates`
7. `coverage_metrics`
8. `source_classes_priority`
9. `suspected_stress_layers`
10. `confidence`

## Rule

The execution step must stay inside:

1. the expansion plan query seeds
2. the suspected stress layers
3. the negative boundaries

It should not expand to unrelated systems.

## Open Questions

1. Should v1 require a minimum matched-artifact count before a bounded research
   set is considered usable?
2. Should the next step rank entity candidates or just preserve them as a set?
