# Trade Press Cluster And Merge V2 Assessment

Date: 2026-03-21

## Inputs
- Capital-flow batch:
  - `research/archive/normalized/trade_press/trade_press_gpt4omini_v7_30.json`
- Energy-flow batch:
  - `research/archive/normalized/trade_press/trade_press_energy_flow_gpt4omini_v11_30.json`
- Shared prefilter batch:
  - `research/archive/normalized/trade_press/trade_press_prefilter_v5_30.json`

## Outputs
- Capital-flow clusters:
  - `research/archive/normalized/trade_press/trade_press_capital_flow_clusters_v2.json`
- Energy-flow clusters:
  - `research/archive/normalized/trade_press/trade_press_energy_flow_clusters_v2.json`
- Structural-pressure candidates:
  - `research/archive/normalized/trade_press/trade_press_structural_pressure_candidates_v2.json`

## Metrics

### Capital-flow clustering
- input signals: `40`
- clusters: `4`

### Energy-flow clustering
- input signals: `51`
- clusters: `6`

### Structural-pressure merge
- capital clusters: `4`
- energy clusters: `6`
- structural-pressure candidates: `6`
- held-upstream energy clusters: `1`

## Current Structural Pressure Map
- `data center power demand buildout`
- `grid equipment and transformer pressure`
- `industrial manufacturing expansion`
- `power generation and backup equipment pressure`
- `utility and large-load power demand pressure` (`2025-04-07` window)
- `utility and large-load power demand pressure` (`2025-10-30` window)

## What Improved
- duplicate structural-pressure candidates were eliminated
- generic energy-only pressure no longer auto-promotes
- capital-only industrial clusters remain possible
- energy-only generic pressure is now held upstream

## Important Interpretation
- `capital_flow_cluster` remains the primary lane
- `energy_flow_pressure_cluster` reinforces when system and time overlap
- generic energy-only pressure should stay upstream until it becomes more concrete

## Remaining Limitations
- system labeling is still heuristic and coarse
- repeated same-source-class trade-press signals can still dominate a cluster
- no source-diversity weighting exists yet
- no explicit analyst audit has been written for the `v2` structural-pressure candidate set
