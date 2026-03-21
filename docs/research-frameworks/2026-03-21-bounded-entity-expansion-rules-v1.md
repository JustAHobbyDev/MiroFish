# Bounded Entity Expansion Rules v1

Date: March 21, 2026

## Purpose

Define the first deterministic downstream expansion step from:

1. `corporate_family_candidate`
2. approved initial priority entity list

## Facts

1. Not every bounded entity should immediately become a filing target.
2. The first downstream pass should stay narrow and explicit.
3. The already-audited transformer lane provides the right first test.

## Rule

`v1` expansion should:

1. only use entities explicitly listed in the first downstream assessment
2. preserve local source coverage already found
3. mark missing source classes, especially `company_filing`

## Output

A `bounded_entity_expansion` should include:

1. canonical entity name
2. member entities
3. supporting artifacts
4. local source coverage
5. filing gap
6. next priority source classes

## Open Questions

1. Should `2+` local source classes be mandatory before filing expansion?
2. Should `v2` include deterministic ticker hints or only company names?

