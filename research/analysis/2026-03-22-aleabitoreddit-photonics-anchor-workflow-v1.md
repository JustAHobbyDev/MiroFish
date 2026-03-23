# AleaBito Photonics Anchor Workflow v1

Date: March 22, 2026

Purpose:

- reconstruct the photonics discovery path from the local X archive
- determine whether `LITE`, `AAOI`, and `COHR` were starting points or downstream expressions
- convert the observed chronology into a practical workflow hypothesis for MiroFish

Primary input:

- [aleabitoreddit-daily-archive-v1.json](/Users/danielschmidt/dev/MiroFish/research/analysis/aleabitoreddit-daily-archive-v1.json)

Related notes:

- [2026-03-19-aleabitoreddit-methods-archaeology-aaoi-lite-iqe-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-19-aleabitoreddit-methods-archaeology-aaoi-lite-iqe-v1.md)
- [2026-03-19-aleabitoreddit-methods-archaeology-cohr-poet-sive-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-19-aleabitoreddit-methods-archaeology-cohr-poet-sive-v1.md)

## Facts

### Earliest relevant chronology

1. `LITE` appears first as the initial anchor clue
- `2025-10-25T06:17:21Z`
- id: `1981968303271592379`
- text:
  - `First time I’ve heard of $LITE, seems interesting I’ll take a look over the weekend`

2. TPU / Ironwood research appears before the photonics chain is fully named
- `2025-11-29T01:23:36Z`
- id: `1994577956598141333`
- text references:
  - `TPU v7 Ironwood`
  - `NVDA Blackwell`

3. The supply-chain frame becomes explicit before `AAOI`, `COHR`, or `AXTI` are fully explained
- `2025-12-01T17:21:19Z`
- id: `1995543748353347989`
- text starts:
  - `Analysis of the $GOOGL TPU v7 Ironwood Suppliers`

4. `COHR` appears before `AAOI` and before `AXTI`
- first exact `$COHR` mention:
  - `2025-12-05T05:14:28Z`
  - id: `1996810382875177099`
- context:
  - appears inside a portfolio list for `TPU/GPU ramp`
  - not as a newly discovered bottleneck

5. `AAOI` appears after `LITE` and after the TPU supplier-map work
- first exact `$AAOI` mention:
  - `2025-12-11T22:18:06Z`
  - id: `1999242313735016715`
- text:
  - `... didn't like it as much compared to $AAOI given AAOI already has direct hyperscaler customers with $MSFT and $AMZN`

6. `AAOI` is immediately framed as a leveraged downstream expression
- `2025-12-11T23:06:02Z`
- id: `1999254375601177015`
- text:
  - `... the alpha for $AAOI is that $MSFT Maia 200 orders were more of R&D ...`

7. The full `LITE` thesis is published before `AXTI`
- `2025-12-22T08:27:15Z`
- id: `2003019490871869644`
- text starts:
  - `The $LITE thesis: The hidden monopoly in the AI.`

8. On the same day, `AAOI` and `COHR` are framed relative to `LITE`
- `2025-12-22T13:00:24Z`
- id: `2003088229147533645`
- text:
  - `$LITE and $COHR are basically duopolies in photonics`
  - `Then there's $AAOI, extreme alpha + leverage call on $MSFT + $AMZN hyperscaler ASICs`

9. `AXTI` appears only after `LITE` is already legible
- first exact `$AXTI` mention:
  - `2025-12-22T09:48:57Z`
  - id: `2003040048930074770`
- text:
  - `Another good one is $AXTI which is the materials supplier for $LITE / photonics. $500m mc`

10. The explicit bottleneck thesis comes later still
- `2025-12-26T15:08:13Z`
- id: `2004569946492453003`
- text starts:
  - `Warning: The entire AI industry will likely be bottlenecked by two companies`

### Role reads from the chronology

1. `LITE`
- role:
  - `anchor expression`
- why:
  - first photonics-specific company clue
  - tied to TPU / Ironwood / Blackwell system research
  - becomes the reference point for later names

2. `COHR`
- role:
  - `adjacent compounder / adjacent anchor`
- why:
  - appears as part of the same photonics field
  - framed as a duopoly partner to `LITE`
  - not introduced as the hidden source of the chain

3. `AAOI`
- role:
  - `levered adjacent expression`
- why:
  - appears after the chain is already being understood
  - framed through customer exposure:
    - `MSFT Maia`
    - `AMZN Trainium`
  - repeatedly described as more asymmetric but riskier than `LITE`

4. `AXTI`
- role:
  - `hidden upstream chokepoint`
- why:
  - introduced as supplier to `LITE / photonics`
  - later upgraded into the explicit InP bottleneck thesis

## Comparative Read

### What clearly did not happen

1. The workflow did not start with `AXTI`.
2. It did not start with a raw materials bottleneck in isolation.
3. It did not jump directly from broad photonics buzzwords to the final upstream chokepoint.

### What appears to have happened

1. A visible company clue appears:
  - `LITE`
2. System research makes that clue legible:
  - `TPU v7 Ironwood`
  - `Blackwell`
  - later `Trainium`
3. Adjacent expressions are formed:
  - `COHR`
  - `AAOI`
4. Only after the downstream map is coherent does the workflow move upstream:
  - `AXTI`

## Workflow Hypothesis

The observed photonics path is:

1. `anchor clue detection`
- notice an already-visible company tied to the system transition
- example:
  - `LITE`

2. `system-demand mapping`
- map the buildout driver first
- example:
  - `TPU v7 Ironwood`
  - `Blackwell`
  - `Trainium`

3. `anchor expression confirmation`
- confirm the anchor sits near the center of the system
- example:
  - repeated `LITE` BOM and supplier-map framing

4. `adjacent expression expansion`
- look for:
  - safer adjacent anchors
  - more leveraged downstream expressions
- examples:
  - `COHR`
  - `AAOI`

5. `upstream chokepoint tracing`
- walk upstream from the confirmed anchor rather than from the theme in the abstract
- example:
  - `LITE -> AXTI`

6. `second-order refinement`
- once the chokepoint is clear, search for adjacent upstream layers
- example:
  - `IQE`

## Product Implication

The current MiroFish blind workflow is too bottleneck-first.

A better workflow hypothesis is:

1. detect `anchor expressions` from real in-window evidence
2. build a dependency map from the anchor
3. generate:
  - `adjacent expressions`
  - `upstream chokepoints`
4. only then rank final expressions

This matches the archive more closely than trying to surface obscure upstream names directly from sparse mixed-source evidence.

## Assumptions

1. Archive chronology is a usable proxy for AleaBito's true research order.
2. Public posting lag is not so large that it inverts the visible order.
3. The photonics workflow is representative enough to inform product design.

## Speculative

1. The most important failure in the recent blind run may be missing `anchor clue detection`, not just insufficient source volume.
2. A system that cannot surface `LITE`-type anchors early will likely fail to surface `AXTI`-type chokepoints honestly.
3. The next product experiment should likely be:
  - `anchor -> adjacency -> upstream`
  rather than:
  - `theme -> direct bottleneck`

## Open Questions

1. Do we want to formalize `anchor_expression` as a first-class object in the pipeline?
2. Should `COHR` be treated as a separate subtype from `LITE`, or is `adjacent_anchor` enough for now?
3. Do we want the next archaeology pass to map:
  - `AAOI`
  - `COHR`
  - `AXTI`
  into a single photonics dependency graph artifact?
