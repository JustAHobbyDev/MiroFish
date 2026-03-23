# Codex Handoff For MiroFish vNext

Date: March 22, 2026

## Purpose

This document is the kickoff handoff for the new standalone `vnext` repository.

Use it at the start of the next Codex thread after `vnext/` has been moved or
copied into its own repo.

## Current Position

### Facts

1. The prior repo accumulated significant conceptual debt.
2. Synthetic data materially distorted earlier progress claims.
3. The most important real insight recovered from the recent work is:
   - the system needs to start from a real clue
   - build a graph from that clue
   - score nodes on that graph for underappreciation and structural leverage
4. The exact route shape is secondary.
5. The critical requirement is that a route exists at all and can be traversed
   into candidate nodes that can be evaluated for undervaluation.

### Conclusion

The new project should be treated as a reset, not a continuation of the full
legacy pipeline.

## vNext Goal

Prove that the system can:

1. capture a real clue
2. build a graph from that clue
3. surface connected candidate nodes
4. rank the most underappreciated node early enough to matter

## Active Scope

Only four areas are in scope:

1. `clues`
2. `graph`
3. `scoring`
4. `benchmarks`

## Not In Scope

Do not spend time on these unless they become directly necessary for the proof:

1. execution policy
2. options-expression logic
3. lane taxonomy expansion
4. large downstream formatting layers
5. speculative broad-web ingestion programs

## Files To Read First

Read these before writing code:

1. [vnext/README.md](/Users/danielschmidt/dev/MiroFish/vnext/README.md)
2. [2026-03-22-mirofish-vnext-core-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-22-mirofish-vnext-core-v1.md)
3. [2026-03-22-mirofish-vnext-reset-triage-v1.md](/Users/danielschmidt/dev/MiroFish/docs/research-frameworks/2026-03-22-mirofish-vnext-reset-triage-v1.md)
4. [2026-03-22-anchor-workflow-comparison-photonics-memory-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-22-anchor-workflow-comparison-photonics-memory-v1.md)
5. [2026-03-22-aleabitoreddit-photonics-anchor-workflow-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-22-aleabitoreddit-photonics-anchor-workflow-v1.md)
6. [2026-03-22-aleabitoreddit-memory-anchor-workflow-v1.md](/Users/danielschmidt/dev/MiroFish/research/analysis/2026-03-22-aleabitoreddit-memory-anchor-workflow-v1.md)

## Important Lessons Already Learned

### Facts

1. `Photonics` and `memory` do not share the same sequence.
2. Both still reduce to:
   - observable clue
   - graph expansion
   - candidate nodes
   - expression selection
3. The photonics replay only recovered `AXT` after the real filings were
   actually present.
4. Therefore the main bottleneck is evidence capture quality plus graph
   construction, not richer downstream formatting.

### Product Implication

Do not design the new repo around many workflow families first.

Instead design around:

1. graphable clues
2. graph edges
3. graph nodes
4. node scoring

## Minimal Objects To Implement First

### `clue`

Required fields:

1. `clue_id`
2. `clue_type`
3. `observed_at`
4. `source_class`
5. `source_url`
6. `text_span`
7. `theme_hint`
8. `evidence_confidence`

### `graph_node`

Required fields:

1. `node_id`
2. `node_type`
3. `canonical_name`
4. `market_type`
5. `source_support_count`
6. `is_public`

### `graph_edge`

Required fields:

1. `edge_id`
2. `source_node_id`
3. `target_node_id`
4. `edge_type`
5. `evidence_artifact_ids`
6. `confidence`

### `node_score`

Required fields:

1. `node_id`
2. `constraint_score`
3. `sensitivity_score`
4. `neglect_score`
5. `expression_score`
6. `composite_score`
7. `score_notes`

## Initial Edge Vocabulary

Keep it small:

1. `supplier_of`
2. `customer_of`
3. `partner_of`
4. `capacity_for`
5. `depends_on`
6. `bottleneck_to`
7. `proxy_for`

## Recommended First Development Steps

1. Create a minimal Python package and test harness for:
   - `clue`
   - `graph_node`
   - `graph_edge`
   - `node_score`
2. Implement a tiny graph builder that starts from one benchmark clue and emits
   a graph artifact.
3. Use one benchmark first:
   - `photonics`
4. Keep the first graph very small and explicit:
   - `Lumentum`
   - `Coherent`
   - `AXT`
   - `JX Advanced Metals`
5. Add the first node scoring pass on that graph.
6. Only after that, replay the memory case and compare how the same graph and
   scoring abstractions hold up.

## Recommended Benchmark Order

1. `photonics`
   - best first case for graph traversal to upstream chokepoint
2. `memory`
   - best second case for stress-testing whether the same graph objects work on
     a cycle-driven setup

## Hard Rules For The New Repo

1. No synthetic evidence in evaluation paths.
2. No module lands unless it improves:
   - clue capture
   - graph quality
   - node scoring
   - benchmark evaluation
3. Prefer explicit benchmark artifacts over broad infrastructure.
4. Keep object count low until the proof path is working.

## Assumptions

1. The new repo should start small and stay small until it proves something
   real.
2. The goal is not to port the old system.
3. The goal is to prove the core loop with less conceptual drag.

## Speculative

1. Later the project may need additional clue families or graph expansions.
2. That should be added only after the first benchmark path is working.

## Open Questions

1. What is the minimum evidence threshold required before a clue should spawn
   graph expansion?
2. What node-score components best capture underappreciation?
3. When should a graph branch be pruned instead of expanded?
