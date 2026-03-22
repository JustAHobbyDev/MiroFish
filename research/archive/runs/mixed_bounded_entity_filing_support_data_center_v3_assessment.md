# Mixed Bounded Entity Filing Support Data Center v3 Assessment

## Facts
1. `9` data-center-lane entities were evaluated for filing support.
2. `9` are filing-supported.
3. The support queue is now split by role lane:
   - `equipment_supplier`: `5`
   - `utility_or_operator`: `4`

## Equipment Supplier Lane
1. `Hitachi Energy`
2. `GE Vernova`
3. `Mitsubishi Electric`
4. `Eaton`
5. `Schneider Electric`

## Utility Or Operator Lane
1. `FirstEnergy`
2. `DTE`
3. `Exelon`
4. `Southern`

## Utility-Specific Evidence
Utility/operator rows now carry deterministic summaries for:
1. load and demand signals
2. grid-response signals
3. capex-response signals

## Outcome
The filing-support layer no longer mixes equipment manufacturers with utility parents in one undifferentiated queue.
