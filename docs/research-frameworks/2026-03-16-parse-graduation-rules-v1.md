# Parse Graduation Rules v1

Date: March 16, 2026

## Purpose

Define when a structural parse should remain:

- `exploratory_only`
- `watchlist_candidate`
- `pick_candidate`

This is the missing bridge between:

- interesting structural graphs
- and a disciplined pick engine

Without this layer, MiroFish can produce compelling market-miss statements but
still lacks a rule for when those statements are strong enough to influence the
actual pick workflow.

## Inputs

Comparison artifact:

- [2026-03-16-parse-graduation-comparison-v1.json](/home/d/codex/MiroFish/research/analysis/2026-03-16-parse-graduation-comparison-v1.json)

Underlying per-pilot outputs:

- [2026-03-16-robotics-actuation-graduation-v1.json](/home/d/codex/MiroFish/research/analysis/2026-03-16-robotics-actuation-graduation-v1.json)
- [2026-03-16-mp-magnet-sovereignty-graduation-v1.json](/home/d/codex/MiroFish/research/analysis/2026-03-16-mp-magnet-sovereignty-graduation-v1.json)
- [2026-03-16-sive-photonics-graduation-v1.json](/home/d/codex/MiroFish/research/analysis/2026-03-16-sive-photonics-graduation-v1.json)

Evaluation script:

- [evaluate_parse_graduation.py](/home/d/codex/MiroFish/scripts/evaluate_parse_graduation.py)

## Rubric dimensions

Each parse is now graded on four dimensions.

### 1. Source mix

Measures:

- share of `evidence`-mode sources
- share of `high`-quality sources
- independent-source presence
- source-class diversity

This is the main filter preventing us from promoting exciting but weakly
corroborated chains too early.

### 2. Structure quality

Measures:

- entity count
- relationship count
- claim count
- evidence-link count
- inference count
- presence of key entity and relationship types

This answers:

- did the parser actually reconstruct a usable causal graph?

### 3. Market-miss quality

Measures:

- presence of a `market_miss` inference
- inference confidence
- number of supporting claims
- number of supporting relationships

This answers:

- did the system produce an actionable stale-market-framing statement, or just a
  descriptive chain?

### 4. Expression readiness

Measures:

- presence of an `ExpressionCandidate`
- `CANDIDATE_EXPRESSION_FOR`
- `REPRICES_VIA`

This answers:

- did the graph get far enough to name a plausible public expression and a
  repricing path?

## Graduation gates

### Exploratory only

This is where a parse should stay if:

- source quality is weak
- or the graph is structurally incomplete
- or the market-miss statement is too thin

Operational meaning:

- useful for idea generation
- not allowed to directly influence final picks
- needs additional external evidence before promotion

### Watchlist candidate

This is where a parse should land if:

- source quality clears a baseline threshold
- the structural graph is strong
- a clear market-miss inference exists
- an expression path is named
- but the source mix is still not high-conviction enough for direct promotion

Operational meaning:

- can enter the structured watchlist
- can influence what we monitor, compare, and deepen
- should not become a high-conviction pick without more corroboration

### Pick candidate

This is the highest promotion tier.

This requires:

- strong source mix
- strong structural graph
- strong market-miss inference
- clear expression readiness
- and `high-conviction` source quality

Operational meaning:

- eligible for direct handoff into the pick engine
- can be ranked against other promoted candidates
- still not an automatic trade, but now belongs inside the actual pick funnel

## Current results

### Robotics actuation

Status:

- `exploratory_only`

Scores:

- source mix: `19.0`
- structure quality: `93.04`
- market-miss quality: `65.0`
- expression readiness: `70.0`

Interpretation:

- the graph itself is good
- the market-miss idea is usable
- but the source base is far too exploratory

This is exactly the correct result.

The robotics pilot is a strong `idea-generation graph`, not a conviction-grade
pick input.

### MP magnet sovereignty

Status:

- `pick_candidate`

Scores:

- source mix: `92.0`
- structure quality: `100.0`
- market-miss quality: `95.0`
- expression readiness: `100.0`

Interpretation:

- this is the cleanest current parse in the repo
- the source mix is strong enough
- the structural graph is complete enough
- the stale-market-framing inference is explicit and well-supported
- the listed expression is already clear

This is the first parse that deserves to directly influence the pick engine.

### SIVE photonics

Status:

- `watchlist_candidate`

Scores:

- source mix: `69.5`
- structure quality: `93.39`
- market-miss quality: `84.17`
- expression readiness: `100.0`

Interpretation:

- the structural graph is strong
- the hidden-supplier rerating inference is strong
- the expression path is clear
- the weak point is corroboration quality, because the source mix is still too
  company-controlled

This is also the correct result.

`SIVE` looks exactly like the kind of idea we want to surface, but not yet one
we should treat as a fully promoted pick without more independent confirmation.

## Why this matters

This solves a real problem in the current system.

Before this rubric, all good-looking parses risked feeling equally persuasive.

Now we have a disciplined distinction between:

- `good structural idea`
- `worth watching`
- `strong enough to promote`

That is essential if the goal is to build a real pick engine rather than a
collection of attractive narratives.

## Current operating rule

Use this default behavior:

- `exploratory_only`
  - keep in research universe
  - do not rank with promoted picks

- `watchlist_candidate`
  - add to monitored candidate set
  - seek independent corroboration or market-data validation

- `pick_candidate`
  - allow direct handoff into the pick-ranking workflow
  - compare against other promoted names on stock vs LEAPS expression

## Most valuable next move

Take the graduation rule seriously and use it as a gate.

That means:

1. only `pick_candidate` parses can flow straight into final ranking
2. `watchlist_candidate` parses need a defined corroboration step
3. `exploratory_only` parses should be treated as universe-building material

The next implementation step should be to connect this rubric to the pick
pipeline so promoted parses can feed candidate rows automatically.
