# Company Filing Expansion Rules v1

Date: March 21, 2026

## Purpose

Define the first deterministic filing-expansion step from:

1. selected bounded entity expansions
2. into explicit company-filing collection plans

## Facts

1. The first transformer-lane entity set is ready for filing-focused follow-up.
2. The local archive does not yet contain company-filing support for those entities.
3. The next honest step is to make the issuer-resolution and filing-route gap explicit.

## Rule

Every filing-expansion plan should:

1. carry forward bounded-system provenance
2. preserve supporting local artifacts
3. mark issuer identity as unresolved unless formally resolved
4. mark filing collection as not yet collected until actual filing retrieval occurs

## Required Fields

1. `company_filing_expansion_plan_id`
2. `canonical_entity_name`
3. `system_label`
4. `priority_tier`
5. `origin_corporate_family_candidate_id`
6. `member_entities`
7. `local_source_classes`
8. `issuer_resolution_status`
9. `company_filing_status`
10. `candidate_filing_form_sets`
11. `resolution_tasks`
12. `collection_gate`

## Open Questions

1. Should `v2` include deterministic issuer-resolution hints from local artifacts?
2. Should foreign-current-report handling expand beyond `20-F` once live filing collection starts?

