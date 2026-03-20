# AleaBito Methods Archaeology: `COHR`, `POET`, `SIVE`

Date: March 19, 2026

Purpose:

- extend the chain-role archaeology beyond `LITE`, `AAOI`, `AXTI`, and `IQE`
- determine how `COHR`, `POET`, and `SIVE` function inside the photonics workflow
- separate core chain roles from adjacent observed subtypes

Primary inputs:

- [aleabitoreddit-daily-archive-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/aleabitoreddit-daily-archive-v1.json)
- [extract_x_expression_context.py](/Users/danielschmidt/dev/MiroFish/scripts/extract_x_expression_context.py)
- local derived context file: `research/analysis/aleabitoreddit-expression-context-cohr-poet-sive-v1.json`
- prior archaeology notes:
  - [2026-03-19-aleabitoreddit-methods-archaeology-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-19-aleabitoreddit-methods-archaeology-v1.md)
  - [2026-03-19-aleabitoreddit-methods-archaeology-aaoi-lite-iqe-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-19-aleabitoreddit-methods-archaeology-aaoi-lite-iqe-v1.md)

## Facts

### `COHR` behaves like a safer system anchor / compounder

Top context terms:

- `capacity`
- `supply chain`
- `research`
- `thesis`
- `mapping`

Representative cues:

- repeated `LITE` / `COHR` duopoly framing
- described as showing up across future bottlenecks
- often used as a safer or more defensible long than smaller-cap photonics names
- tied to downstream pricing power and US optical manufacturing relevance

Interpretation:

- `COHR` is not treated as the hidden chokepoint
- it is also not framed as the most levered asymmetry
- it functions as a durable anchor or compounder inside the same chain

Best role read:

- adjacent `system_anchor`

### `POET` behaves like a speculative workaround branch

Top context terms:

- `earnings`
- `supply chain`
- `qualification`
- `customers`
- `benchmark`

Representative cues:

- compared negatively against `AAOI` because of weaker hyperscaler qualification
- described as a workaround path to lower `InP` usage rather than the core current bottleneck
- repeatedly framed as earlier-stage, speculative, and more retail-crowded
- later treated as opportunity after financing events, but still not the main photonics expression

Interpretation:

- `POET` is not part of the first bottleneck-discovery chain
- it appears as a workaround or architecture-branch speculation
- the bet is more about future adoption timing and execution than current chokepoint control

Best role read:

- speculative workaround branch

### `SIVE` behaves like a later-cycle follow-on expression

Top context terms:

- `thesis`
- `capacity`
- `customers`

Representative cues:

- first explicit mention says the author does not know the company yet
- much later returns as a full promoted long
- framed as `the next LITE` for silicon photonics / CPO
- justified through supplier status to newer CPO / silicon-photonics names rather than current EML bottlenecks

Interpretation:

- `SIVE` is clearly not part of the original photonics discovery wave
- it arrives after the photonics chain is already legible
- it is a follow-on expression for the next architecture leg, not the first bottleneck itself

Best role read:

- later-cycle follow-on expression

## Comparative Read

### Core roles that appear stable enough to formalize now

These are the role labels that recur across both archaeology and current product needs:

1. `system_anchor`
2. `levered_adjacent_expression`
3. `hidden_upstream_bottleneck`
4. `second_order_upstream_refinement`

### Observed adjacent subtypes

These appear real in the archive, but are not yet stable enough to force into the
first product contract:

1. safer compounder anchor
   - `COHR`
2. speculative workaround branch
   - `POET`
3. later-cycle follow-on expression
   - `SIVE`

## Product Implication

The first product-side role model should stay narrow.

Reason:

- the four core roles above are easier to infer from current structural artifacts
- `COHR`, `POET`, and `SIVE` suggest real extensions, but they rely on subtler
  timing and architecture-branch context
- forcing those extensions into the first deterministic classifier would add
  fake precision

Pragmatic rule:

1. formalize the four core roles now
2. keep the adjacent subtypes in research notes
3. promote them into the ontology only after we can score them from artifact data

## Speculative Ideas

- `COHR` may represent a class of expression that is less about hiddenness and
  more about repeated appearance across multiple future bottlenecks.
- `POET` may represent a useful explicit class of `workaround candidate` once the
  system starts tracking substitute architectures.
- `SIVE` may represent a future `next-wave expression` class for later-cycle
  rotation logic.

## Open Questions

1. Do we want to add a distinct `workaround candidate` role once substitute-path
   tracking is stronger?
2. Do we want a later-cycle rotation workflow separate from the initial
   bottleneck-discovery workflow?
3. Should `COHR` eventually be split out from `system_anchor` into a more
   specific `defensible compounder anchor` label?
