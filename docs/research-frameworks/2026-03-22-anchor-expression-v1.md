# Anchor Expression v1

Purpose:

- surface visible system anchors before upstream bottleneck inference
- create a deterministic object that sits earlier than bounded-universe promotion
- make anchor-first replay possible on sparse real historical corpora

Current scope:

- profile-driven
- first implemented profile:
  - `photonics`

Inputs:

- one or more real prefilter batches
- by default:
  - `kept_artifacts`
  - `review_artifacts`
- synthetic artifacts excluded by default

Output object:

- `anchor_expression_candidate`

Core fields:

- `canonical_entity_name`
- `anchor_role`
- `supporting_artifact_ids`
- `supporting_titles`
- `mentioned_entities`
- `source_classes`
- `support_count`
- `max_anchor_score`

Current `photonics` role labels:

1. `anchor_expression`
2. `adjacent_anchor`
3. `upstream_dependency`

Boundary:

- system-demand drivers like `NVIDIA` are not emitted as anchor expressions
- they remain context, not expressions

Why this exists:

- the archive-backed AleaBito reconstruction shows the path was:
  - anchor clue
  - system map
  - adjacent expressions
  - upstream chokepoint
- not:
  - direct obscure bottleneck discovery from sparse corpus evidence
