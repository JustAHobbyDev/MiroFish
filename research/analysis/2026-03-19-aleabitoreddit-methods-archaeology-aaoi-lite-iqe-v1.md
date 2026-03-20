# AleaBito Methods Archaeology: `AAOI`, `LITE`, `IQE`

Date: March 19, 2026

Purpose:

- extend the methods archaeology beyond `AXTI` and `SNDK`
- classify how `AAOI`, `LITE`, and `IQE` function inside the photonics discovery chain
- determine whether they cluster with the `AXTI` bottleneck workflow or reveal distinct subtypes

Primary inputs:

- [aleabitoreddit-daily-archive-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/aleabitoreddit-daily-archive-v1.json)
- [extract_x_expression_context.py](/Users/danielschmidt/dev/MiroFish/scripts/extract_x_expression_context.py)
- local derived context file: `research/analysis/aleabitoreddit-expression-context-aaoi-lite-iqe-v1.json`
- prior archaeology note:
  - [2026-03-19-aleabitoreddit-methods-archaeology-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-19-aleabitoreddit-methods-archaeology-v1.md)

## Facts

### `LITE` is the visible beneficiary / system anchor

Top context terms:

- `thesis`
- `capacity`
- `supply chain`
- `BOM`
- `earnings`
- `research`

Representative cues:

- TPU v7 supply-chain research
- direct thesis framing around `LITE`
- repeated `BOM` references
- earnings spillover from `AVGO`
- later downstream consequences from `AXTI` / export-control bottlenecks

Interpretation:

- `LITE` is the visible, obvious beneficiary that anchors the chain
- it is where the photonics thesis becomes legible
- it is not the hidden chokepoint
- it is the name that makes the broader buildout concrete

Best role label:

- `system anchor`

### `AAOI` is the adjacent leveraged downstream expression

Top context terms:

- `capacity`
- `earnings`
- `BOM`
- `thesis`
- `supply chain`

Representative cues:

- direct hyperscaler-customer references
- repeated framing as a levered `MSFT / AMZN` play
- `BOM`-based comparisons against `LITE`
- conference and catalyst references
- very strong later earnings-driven re-rating

Interpretation:

- `AAOI` is not discovered as the root bottleneck
- it is framed as a more asymmetric downstream expression tied to specific hyperscaler ramps
- it sits one step away from `LITE`, offering more upside and more execution risk

Best role label:

- `levered adjacent expression`

### `IQE` is the second-order upstream refinement

Top context terms:

- `capacity`
- `earnings`
- `BOM`
- `supply chain`
- `DD`
- `mapping`

Representative cues:

- introduced after `AXTI` had already worked
- relationship map:
  - `GOOGL -> LITE -> IQE -> AXTI`
- repeated focus on epiwafer capacity, debt, restructuring, and foundry economics
- often inferred through upstream mapping rather than directly confirmed

Interpretation:

- `IQE` is not the first hidden bottleneck
- it is a second-order refinement after the chain is already understood
- it comes from asking whether there is another underfollowed upstream layer above or beside the already-discovered one

Best role label:

- `second-order upstream refinement`

## Comparative Read

### What clusters with `AXTI`

`IQE` is closest to `AXTI`, but not identical.

Common features:

- supply-chain mapping
- upstream industrial role
- capacity constraints
- hidden importance relative to valuation

Difference:

- `AXTI` is framed as the chokepoint itself
- `IQE` is framed as an upstream-adjacent refinement with more balance-sheet and execution caveats

### What does not cluster with `AXTI`

`LITE` and `AAOI` do not look like pure bottleneck-discovery names.

Reason:

- both are downstream of the rawest chokepoint layer
- both are framed more through:
  - demand flow
  - customer exposure
  - BOM share
  - earnings/capacity scaling

They are expression-selection names, not bottleneck-identification names.

## Strongest Current Hypothesis

Inside photonics, AleaBito appears to use a chain with at least four distinct roles:

1. `system anchor`
   - example: `LITE`

2. `levered adjacent expression`
   - example: `AAOI`

3. `hidden upstream bottleneck`
   - example: `AXTI`

4. `second-order upstream refinement`
   - example: `IQE`

This is a stronger model than treating all photonics names as one homogeneous bucket.

## Product Implication

The product likely needs to reason about `role in chain`, not just `relevance to theme`.

At minimum, the engine should be able to distinguish:

1. visible beneficiary
2. adjacent leveraged expression
3. hidden upstream bottleneck
4. second-order refinement

That matters because each role implies a different evidence standard:

- `LITE`
  - needs system-demand confirmation and BOM significance
- `AAOI`
  - needs customer/ramp/earnings confirmation
- `AXTI`
  - needs concentration, supply-chain, and chokepoint proof
- `IQE`
  - needs refinement mapping, capacity, and restructuring proof

## Speculative Ideas

- A large part of AleaBito's edge may be not just finding the right theme, but finding the right `role` within the chain.
- The highest-upside names may often be those where the role is misclassified by the market:
  - a hidden bottleneck treated like a commodity
  - a levered expression treated like a low-quality follower
  - a refinement layer ignored because the first bottleneck already moved

## Open Questions

1. Do we want to formalize these as explicit chain-role labels in the product?
2. Do we want to extend the same role analysis to:
   - `COHR`
   - `POET`
   - `SIVE`
3. Do we want the next archaeology pass to classify all major AleaBito expressions by:
   - discovery workflow
   - chain role
   - evidence standard
