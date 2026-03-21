# Southern Dual-Role Test v1

## Artifact
- `As load grows, Southern raises spending plan to $81B`

## Facts
- The article states:
  - Southern raised its five-year spending plan to `$81B`
  - the increase is driven by growth infrastructure investments
  - large-load and data-center demand are increasing
  - the company is working on adding `10GW` of approved new generation

## Test
- Decide whether this artifact should be modeled as:
  - `capital_flow_signal_candidate`
  - `energy_flow_pressure_signal`
  - or both

## Result
- `capital_flow_signal_candidate`: `yes`
- `energy_flow_pressure_signal`: `yes`
- recommended relationship:
  - `energy_flow_pressure_and_capital_flow`

## Why

### Capital-flow basis
- explicit five-year spending-plan increase
- direct infrastructure-investment language
- approved generation additions

### Energy-flow-pressure basis
- explicit load growth
- explicit data-center demand
- explicit generation-response need

## Decision
- Southern-like utility spending-plan artifacts should be treated as
  dual-role artifacts.
- They carry:
  - direct capital-flow evidence
  - and direct energy-flow-pressure evidence

## Implication
- This gives a clean boundary:
  - utility pipeline and forecast articles remain `energy_flow_pressure_only`
  - utility spending-plan or signed-demand articles can become:
    - `energy_flow_pressure_and_capital_flow`
