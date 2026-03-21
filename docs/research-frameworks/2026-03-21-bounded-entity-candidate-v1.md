# Bounded Entity Candidate v1

Date: March 21, 2026

## Purpose

Define the first deterministic downstream entity object produced from a
`bounded_research_set`.

## Facts

1. A bounded research set still contains mixed artifact evidence.
2. The next practical step is to identify visible beneficiary or supplier
   entities inside that bounded lane.
3. This step should stay deterministic and auditable.

## Definition

A `bounded_entity_candidate` is a deterministic entity-level object built from:

1. one `bounded_research_set`
2. matched supporting artifacts
3. title or issuer-derived entity hints

## Required Fields

1. `bounded_entity_candidate_id`
2. `origin_bounded_research_set_id`
3. `system_label`
4. `entity_name`
5. `entity_role`
6. `artifact_support_count`
7. `source_classes`
8. `supporting_artifact_ids`
9. `supporting_titles`
10. `matched_terms`
11. `priority_tier`
12. `recommended_next_source_classes`

## Rule

This step should:

1. preserve bounded-lane discipline
2. prefer entities with explicit supporting artifacts
3. avoid freeform company expansion outside the bounded lane

## Open Questions

1. Should a bounded entity require `2+` artifacts before it is considered
   filing-ready?
2. Should v2 separate visible beneficiaries from enabling suppliers?
3. Should corporate-family normalization happen before or after bounded entity
   formation?
