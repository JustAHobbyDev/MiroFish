# Mixed Bounded Entity Candidates v2 Assessment

## Facts
1. `mixed_bounded_entity_candidates_v2.json` contains `56` bounded entity candidates across three bounded lanes.
2. The exploratory utility lane contributes `18` raw candidates.

## Utility Lane Read
The utility lane now contains real operator names worth keeping:

1. `DTE`
2. `FirstEnergy`
3. `Southern`
4. `Exelon`
5. `CyrusOne`

## Important Boundary
The raw utility candidate set also contains:

1. real supplier names that belong in supplier lanes
2. synthetic fixture entities from the local corpus

So the raw utility candidate set should not drive live filing work directly.

## Outcome
The utility lane now has enough bounded entity coverage to create a filtered live follow-up queue, but not enough cleanliness to skip that filter.
