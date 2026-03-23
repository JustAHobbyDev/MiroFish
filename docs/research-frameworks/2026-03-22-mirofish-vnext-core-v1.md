# MiroFish vNext Core v1

Date: March 22, 2026

## Purpose

Define the smallest credible next project for MiroFish based on the recent
failures and recoveries.

This is a reset document, not an extension of the current pipeline.

## Facts

1. Synthetic archive inputs overstated progress.
2. The real blind power run did not produce promotion-ready universes.
3. The photonics replay only recovered `AXT` once the real filing evidence was
   actually present.
4. The photonics and memory cases do not share the same route shape.
5. The common structure across both cases is still:
   - observable clue
   - graph expansion
   - candidate nodes
   - selection of the most mispriced node

## Conclusion

vNext should optimize for:

1. finding real clues
2. building a graph from those clues
3. scoring graph nodes for underappreciation and structural leverage
4. benchmarking the result against known AleaBito cases

vNext should not optimize for:

1. lane taxonomy growth
2. downstream handoff formatting
3. elaborate routing abstractions
4. execution policy layers

## Core Loop

1. `clue_capture`
- capture real, in-window evidence that makes a theme legible

2. `graph_build`
- expand from the clue into connected entities and edge types

3. `node_score`
- score nodes for:
  - dependency centrality
  - demand sensitivity
  - bottleneck power
  - neglect / underappreciation
  - expression quality

4. `benchmark_eval`
- compare surfaced nodes against historical benchmark paths

## Core Objects

### `clue`

Required fields:

- `clue_id`
- `clue_type`
- `observed_at`
- `source_class`
- `source_url`
- `text_span`
- `theme_hint`
- `evidence_confidence`

### `graph_node`

Required fields:

- `node_id`
- `node_type`
- `canonical_name`
- `market_type`
- `source_support_count`
- `is_public`

### `graph_edge`

Required fields:

- `edge_id`
- `source_node_id`
- `target_node_id`
- `edge_type`
- `evidence_artifact_ids`
- `confidence`

### `node_score`

Required fields:

- `node_id`
- `constraint_score`
- `sensitivity_score`
- `neglect_score`
- `expression_score`
- `composite_score`
- `score_notes`

### `benchmark_result`

Required fields:

- `benchmark_case`
- `clue_detected`
- `graph_reached_target_node`
- `candidate_rank`
- `blind_ready`
- `limitations`

## Edge Types

The initial edge vocabulary should stay small:

1. `supplier_of`
2. `customer_of`
3. `partner_of`
4. `capacity_for`
5. `depends_on`
6. `bottleneck_to`
7. `proxy_for`

## Non-Goals

For vNext, explicitly do not build:

1. options or execution-policy machinery
2. broad lane-family taxonomies
3. generic downstream review surfaces
4. large speculative corpora

## Assumptions

1. The desired edge comes from graph construction and node scoring, not from
   formatting the downstream outputs more cleanly.
2. A smaller project boundary will improve iteration speed and judgment.
3. The current repo can host the seed, but the vNext proof path should be
   isolated from legacy machinery.

## Speculative

1. The eventual product may still need multiple clue families.
2. That should emerge from graph behavior, not be designed first.

## Open Questions

1. What minimum evidence is required before a clue can seed graph expansion?
2. What node-score components are most predictive of a good AleaBito-style pick?
3. When should a graph branch be pruned instead of expanded?
