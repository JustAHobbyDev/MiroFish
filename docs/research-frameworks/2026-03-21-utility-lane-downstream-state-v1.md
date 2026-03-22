# Utility Lane Downstream State v1

## Purpose

Consolidate the utility follow-up queue with existing filing support and
private-company routing so the lane has one downstream state object.

## Inputs

1. `bounded_entity_followup_queue`
2. `bounded_entity_filing_support_batch`
3. `private_company_diligence_plan_batch`

## Output

One row per utility-lane entity with:

1. downstream status
2. issuer route
3. filing support state
4. next action

## Statuses

1. `public_filing_supported`
2. `private_company_diligence_required`
