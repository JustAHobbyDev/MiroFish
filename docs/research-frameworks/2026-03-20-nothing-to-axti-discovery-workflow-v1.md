# Nothing-to-AXTI Discovery Workflow v1

Date: March 20, 2026

## Purpose

Define the first concrete discovery workflow for the product:

- start from no preselected ticker
- use only public information
- move from weak signals to a verified upstream bottleneck candidate
- use `AXTI` as the benchmark case, not the target output format

This is a workflow spec.
It is not a final ontology or storage schema.

## Goal

The system should be able to do this:

1. detect a live industrial buildout or stress pattern
2. identify the visible beneficiaries first
3. walk upstream through the dependency chain
4. surface a hidden bottleneck candidate
5. verify that bottleneck with stronger public evidence
6. only then treat the name as a real candidate expression

## Facts

From the AleaBito archive and replay work already in the repo:

1. `AXTI` did not appear as the first object.
   - `LITE` appeared first
   - `AAOI` appeared next
   - `AXTI` appeared after the chain was expanded upstream

2. The full `InP chokepoint` thesis was not available from the X archive alone at the first `AXTI` mention.

3. The useful discovery pattern was:
   - visible beneficiary
   - adjacent supplier
   - upstream candidate
   - external verification
   - formal bottleneck thesis

4. This means the product should not start from:
   - thesis scoring
   - ticker ranking
   - expression optimization

5. The product should start from:
   - signal detection
   - chain expansion
   - bottleneck verification

## Assumptions

1. Public information is sufficient to discover some future `AXTI`-like situations.

2. The edge comes from synthesis and upstream traversal, not secret information.

3. A visible beneficiary often appears before the hidden bottleneck expression.

4. The system does not need to infer a full supercycle label before beginning chain expansion.

5. The first v1 implementation can be partially deterministic and partially analyst-reviewed.

## Non-Goals

This workflow does not attempt to solve:

1. final expression ranking
2. options structure selection
3. trade execution
4. portfolio construction
5. broad multi-theme autonomy from day one

Those are downstream.

## Entry Condition

The true starting point is not `thesis intake`.

The true starting point is:

- `nothing` plus a stream of public signals

In practice, `nothing` means:

- no chosen ticker
- no finalized thesis
- no confirmed bottleneck
- only raw public observations that may or may not matter

## Canonical Workflow

### Stage 1: Signal Detection

Objective:

- identify repeated public observations that may indicate a real industrial buildout, stress pattern, or demand shift

Allowed input classes:

- company filings
- earnings releases and transcripts
- company press releases
- government or policy notices
- trade press
- industry research references surfaced in public posts
- high-signal investor posts

Minimum output:

- a set of `signal candidates`

Each signal candidate must answer:

1. what changed or is changing
2. where it was observed
3. why it might matter physically or economically

Examples:

- TPU ramp commentary
- photonics demand references
- optical component supply tightness
- capacity sold out

Promotion rule:

- one signal is not enough
- move forward only when multiple related signals point to the same emerging system

### Stage 2: Signal Clustering

Objective:

- group related signals into a coherent system or buildout

Minimum output:

- a `signal cluster`

A valid cluster must have:

1. at least one repeated demand or buildout cue
2. at least one repeated supply-chain or component cue
3. a plausible common mechanism

Examples:

- TPU ramp
- photonics components
- optical networking buildout

Promotion rule:

- cluster is strong enough when it can be described as a real system, not just a list of unrelated buzzwords

### Stage 3: Visible Beneficiary Identification

Objective:

- identify the obvious or already-legible names tied to the cluster

This stage is not trying to find the hidden winner yet.

It is trying to answer:

- who is visibly exposed first?

Minimum output:

- a short list of `visible beneficiaries`

Properties:

- likely better known
- often downstream
- often directly tied to demand flow
- useful because they orient the chain

Examples from the photonics benchmark:

- `LITE`
- `COHR`

Promotion rule:

- move forward once at least one visible beneficiary can be linked to the cluster with explicit public evidence

### Stage 4: Chain Expansion

Objective:

- walk upstream from visible beneficiaries to the components, materials, process steps, and suppliers they depend on

This is the critical stage.

Questions:

1. what does the visible beneficiary physically rely on?
2. which components or materials are essential?
3. which suppliers or process layers sit underneath those dependencies?
4. where are there few substitutes, few qualified suppliers, or concentrated capacity?

Minimum output:

- a `dependency chain`

Example pattern:

- demand system
- visible beneficiary
- adjacent supplier
- upstream material or process layer

Example from the photonics benchmark:

- `TPU / AI optical buildout`
- `LITE`
- `AAOI`
- `AXTI`

Promotion rule:

- move forward once at least one upstream company or process layer appears both:
  - structurally necessary
  - less obvious than the visible beneficiary

### Stage 5: Bottleneck Candidate Detection

Objective:

- determine whether any upstream layer in the chain looks constrained enough to deserve bottleneck status

Bottleneck cues:

1. supplier concentration
2. long lead times
3. qualification difficulty
4. low substitutability
5. geographic or policy concentration
6. mismatch between strategic importance and market attention

Minimum output:

- one or more `bottleneck candidates`

Important rule:

- this stage can nominate candidates
- it cannot fully verify them by weak evidence alone

Example from the photonics benchmark:

- `AXTI` as upstream materials supplier before full `InP chokepoint` proof

Promotion rule:

- promote only if the candidate is both:
  - upstream enough to be structurally interesting
  - specific enough to investigate further

### Stage 6: External Verification

Objective:

- verify the candidate with stronger public evidence than timeline chatter or weak thematic correlation

Preferred evidence:

1. filings
2. company disclosures
3. technical manufacturing sources
4. industry-body or trade research
5. public capacity-expansion announcements
6. policy-sensitive geography or export-control evidence

Questions:

1. is the layer actually concentrated?
2. is the company actually exposed to the critical layer?
3. is the constraint current or only hypothetical?
4. is there enough duration for the bottleneck to matter?

Minimum output:

- a `verified bottleneck hypothesis`

Failure rule:

- if stronger evidence does not confirm the bottleneck, the candidate should be downgraded or discarded

### Stage 7: Expression Selection

Objective:

- decide whether the verified bottleneck hypothesis maps cleanly to a public-market expression

This happens only after verification.

Questions:

1. is the company the cleanest listed vehicle?
2. is it a direct bottleneck owner, adjacent supplier, or workaround?
3. is the market likely misclassifying the role?

Minimum output:

- a `candidate expression`

This stage is downstream of discovery.
It is not the first optimization target.

## Required Internal Objects

This is the minimum object set needed for the workflow.

### 1. Signal Candidate

Purpose:

- capture one public observation that may matter

Must include:

1. source provenance
2. time boundary
3. plain-language statement
4. suspected physical or economic implication

### 2. Signal Cluster

Purpose:

- group signals into a coherent buildout or stress pattern

Must include:

1. member signals
2. common mechanism
3. affected system or industry

### 3. Visible Beneficiary

Purpose:

- orient the chain with an obvious exposed company

Must include:

1. company name
2. evidence of direct linkage to the cluster
3. why it is visible rather than hidden

### 4. Dependency Chain

Purpose:

- represent upstream dependencies from the visible beneficiary

Must include:

1. system or component path
2. key process or material layers
3. linked companies where known

### 5. Bottleneck Candidate

Purpose:

- capture an upstream layer or company with credible scarcity potential

Must include:

1. bottleneck cues
2. why the layer matters
3. why the market may not fully appreciate it yet

### 6. Verified Bottleneck Hypothesis

Purpose:

- convert a candidate into a stronger research conclusion

Must include:

1. stronger source support
2. concentration or scarcity proof
3. duration basis
4. exposure path to a public company

## Benchmark Case

Use this first:

- `Photonics -> LITE -> AAOI -> AXTI`

Replay boundary:

- as-of `2025-12-22`

Success standard:

1. the system surfaces `LITE` as a visible beneficiary
2. the system expands the chain upstream
3. the system nominates `AXTI` as an upstream candidate before the later viral chokepoint posts
4. the system requires non-X public evidence before calling the bottleneck verified

This benchmark is passed only if the workflow can separate:

- upstream candidate discovery
- from
- full bottleneck verification

## Product Implications

### What should be built first

1. signal collection and normalization
2. signal clustering
3. visible-beneficiary identification
4. upstream chain expansion
5. bottleneck verification workflow

### What should not be built first

1. complex ranking logic
2. expression scoring depth
3. options selection layers
4. polished pick-engine heuristics

## Failure Modes

1. Theme without chain
   - system finds a narrative but cannot walk upstream

2. Chain without scarcity
   - system maps suppliers but cannot distinguish bottlenecks from ordinary dependencies

3. Scarcity without proof
   - system overpromotes weak candidates from chatter alone

4. Proof without expression
   - system verifies a bottleneck but cannot connect it to a tradable public company

5. Expression without discovery
   - system starts from favored tickers and rationalizes them after the fact

## Speculative Ideas

1. The first product surface may need to look more like a `signal workbench` than a thesis form.

2. A high-quality visible-beneficiary detector may be more important early than a sophisticated expression ranker.

3. The workflow may eventually split into two products:
   - `nothing -> bottleneck discovery`
   - `known cycle -> expression selection`

## Open Questions

1. What should the first bounded public signal universe be for v1:
   - policy-heavy
   - company-heavy
   - trade-press-heavy
   - mixed

2. Should the first implementation start from one domain only:
   - photonics
   - memory
   - critical materials

3. What is the minimum evidence threshold for promoting an upstream name from:
   - visible supplier
   - to bottleneck candidate

4. Which stage should be analyst-reviewed first:
   - signal cluster
   - chain expansion
   - bottleneck verification
