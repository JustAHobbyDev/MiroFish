# Bounded Entity Follow-Up Queue v1

## Purpose

Select the next live downstream queue from bounded entity candidates without
reintroducing synthetic names or cross-lane role mixing.

## Inputs

1. `bounded_entity_candidate_batch`
2. `bounded_entity_filing_support_batch`

## Selection Rule

The queue should only include rows that are:

1. inside one explicit `system_label`
2. `real_only`
3. inside an allowed entity-role set

## Output

One `queue_row` per selected entity with:

1. entity name
2. system label
3. entity role
4. current filing follow-up status
5. next action

## Follow-Up Status

1. `already_supported`
   - existing filing support already exists
   - next action: reuse that support

2. `needs_live_resolution`
   - no filing support exists yet
   - next action: resolve issuer and collect the appropriate route

## Boundary

This queue is not a new ranking layer.
It is a deterministic transition object between bounded entity candidates and
live issuer-resolution or filing work.
