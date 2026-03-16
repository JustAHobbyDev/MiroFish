# Node-Aware Ranking v1

## Purpose

The canonical registry solves identity:

- one underlying node
- multiple thesis pointers

But we also need a review surface that ranks by underlying rather than by
pointer. This layer provides that.

## Inputs

- [knowledge-node registry](/home/d/codex/MiroFish/research/analysis/2026-03-16-knowledge-node-registry-v1.json)

## Output

- [node-aware ranking](/home/d/codex/MiroFish/research/analysis/2026-03-16-node-aware-ranking-v1.json)

## What Each Row Shows

- one `underlying`
- all attached `thesis_pointers`
- `primary_expression_view`
- `alternate_expression_views`
- `expression_conflict`
- strongest supporting:
  - process layers
  - components
  - materials

This means the review surface can now answer:

- what are all the active promoted theses on `MP`?
- what is the strongest current expression view?
- where do expressions conflict?
- which process layers recur across separate theses?

## Current Example

`MP` now appears once in the node-aware ranking with:

- `2` thesis pointers
- primary expression: `shares`
- alternate expression: `leaps_call`
- themes:
  - `Rare Earth Magnet Sovereignty`
  - `Robotics Supply Chain`

That is the intended behavior. The pointer-level ranking is still preserved
separately, but the review surface is now underlying-centric.
