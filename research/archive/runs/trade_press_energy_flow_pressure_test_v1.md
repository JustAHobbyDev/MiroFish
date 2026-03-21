# Trade Press Energy Flow Pressure Test v1

## Facts
- Test set source:
  - [trade_press_gpt4omini_v7_30.json](/Users/danielschmidt/dev/MiroFish/research/archive/normalized/trade_press/trade_press_gpt4omini_v7_30.json)
- Evaluated artifacts:
  - `7` review-stage `no_candidate` utility/load articles
  - `1` review-stage candidate with a signed utility deal
- These articles were correctly held below `capital_flow_signal_candidate` in the final `v7` run.

## Test
- Reinterpret the utility/load articles as:
  - `energy_flow_pressure`
- Do not change the capital-flow labels during the test.
- Ask whether the previously rejected or suppressed articles form a coherent physical-pressure set.

## Results
- artifacts reviewed: `8`
- `energy_flow_pressure`: `8`
- `energy_flow_pressure_only`: `7`
- `energy_flow_pressure_and_capital_flow`: `1`
- `not_energy_flow_pressure`: `0`

## Energy Flow Pressure Only
- PG&E data center pipeline swells to 10GW
- US utility Exelon reports data center pipeline of 33GW
- First Energy data center pipeline surges to 2.6GW by 2029
- PPL Electric's data center pipeline soars to 14GW
- Exelon data center pipeline jumps to 17 GW as load forecast turns positive
- FirstEnergy’s 5-year data center pipeline doubles to 3 GW
- FirstEnergy expects peak load to grow 45% by 2035 on data centers

## Energy Flow Pressure And Capital Flow
- DTE inks first data center deal to grow electric load 25%

## Interpretation
- The suppressed review-stage utility articles are not useless.
- They are weak direct capital-flow artifacts.
- They are strong physical-demand artifacts.
- That means the current capital-flow gate is doing the right job, but it is discarding a distinct upstream signal type.

## Conclusion
- The test supports the distinction.
- `energy_flow_pressure` is a coherent label on real artifacts from the current benchmark.
- The right next design move is not to weaken the capital-flow gate.
- The right next design move is to add a separate upstream object for production-input pressure and let it combine with capital-flow evidence later.

## Open Questions
- Should the first new object be named:
  - `energy_flow_pressure_signal`
  - or the broader
  - `production_input_pressure_signal`
- Should utility spending-plan articles like Southern be modeled as:
  - direct capital-flow only
  - or both capital-flow and energy-flow pressure?
