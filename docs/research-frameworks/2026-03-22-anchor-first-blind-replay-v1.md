# Anchor-First Blind Replay v1

Purpose:

- rerun historical evaluation with an anchor-first workflow
- test whether a sparse real corpus can at least surface anchor clues and adjacent expressions
- avoid overstating hidden bottleneck recovery when upstream evidence is missing

Current use:

- retrospective historical replay
- not a true blind proof

Current output judgments:

1. `anchor_clue_detection`
2. `adjacent_expression_surfacing`
3. `upstream_dependency_surfacing`
4. `hidden_chokepoint_recovery`

Current rule:

- this replay can pass on anchor surfacing while still failing on final hidden chokepoint recovery

Why:

- the desired research sequence is recursive:
  - anchor
  - adjacency
  - upstream
- success at the first stage is useful signal
- but it must not be mislabeled as final-expression success

Boundary:

- if the corpus is retrospective-seeded or missing upstream filings, that limitation must remain explicit in the output
