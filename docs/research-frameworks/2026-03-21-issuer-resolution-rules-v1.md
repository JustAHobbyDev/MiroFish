# Issuer Resolution Rules v1

Date: March 21, 2026

## Purpose

Define the deterministic planning layer between:

1. company-filing expansion plans
2. live issuer-resolution work

## Facts

1. The first filing-expansion queue exists.
2. None of the six selected entities have resolved filing routes yet.
3. The next clean step is to make issuer-resolution paths explicit before any live fetch.

## Rule

This layer may:

1. derive route hints from local artifact text
2. derive foreign geography hints from explicit wording like `Italy-based`
3. generate deterministic issuer-resolution query terms

This layer may not:

1. claim that issuer resolution is complete
2. claim that a filing route is confirmed
3. fetch live filings

## Output

An `issuer_resolution_plan` should include:

1. `canonical_entity_name`
2. `route_hypothesis`
3. `foreign_geography_hints`
4. `candidate_resolution_paths`
5. `issuer_resolution_query_terms`
6. `resolution_queue_group`
7. `issuer_resolution_status`

## Open Questions

1. Should `v2` include deterministic resolution hints from legal suffixes like `plc`, `AG`, or `Ltd`?
2. Should the first live issuer-resolution pass use only official company websites and EDGAR?

