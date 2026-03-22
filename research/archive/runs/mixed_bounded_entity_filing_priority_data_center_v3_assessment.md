# Mixed Bounded Entity Filing Priority Data Center v3 Assessment

## Decision

Advance two separate filing-backed queues:

1. an `equipment_supplier` queue
2. a `utility_or_operator` queue

## Equipment Supplier Queue

1. `Hitachi Energy`
2. `GE Vernova`
3. `Eaton`
4. `Mitsubishi Electric`
5. `Schneider Electric`

## Utility Or Operator Queue

1. `DTE`
2. `FirstEnergy`
3. `Exelon`
4. `Southern`

## Important Boundary

1. `GE Vernova` and `Schneider Electric` now correctly sit in the supplier lane because their supporting titles are manufacturing/buildout artifacts, not utility-load artifacts.
2. Utility parents are now ranked on utility-relevant evidence:
   - load and demand pressure
   - grid response
   - capex response

## Outcome

The data-center filing-backed queue is now structurally cleaner and less prone to cross-role ranking errors.
