# Corporate Family Normalization v1

Date: March 21, 2026

## Purpose

Define a conservative normalization step between:

1. `bounded_entity_candidate`
2. downstream filing or company-expansion work

## Facts

1. Deterministic bounded entity extraction can produce duplicate corporate-family members.
2. Example:
   - `Hitachi`
   - `Hitachi Energy`
3. This duplication should be reduced before broader downstream expansion.

## Rule

`v1` normalization only merges when:

1. one entity name is a whole-token prefix of another
2. both belong to the same bounded system label

This is intentionally conservative.

## Output

A `corporate_family_candidate` should include:

1. `canonical_entity_name`
2. `member_entities`
3. `merge_relation`
4. `normalization_confidence`
5. supporting artifacts and source classes

## Open Questions

1. Should later versions support explicit alias dictionaries?
2. Should subsidiary-specific names sometimes remain unmerged for supplier analysis?

